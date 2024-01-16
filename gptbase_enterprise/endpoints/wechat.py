import asyncio
import json
from datetime import datetime
import httpx
from wechatpy.enterprise import WeChatClient

from starlette.requests import Request
from fastapi import APIRouter, HTTPException
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from typing import Optional
from gptbase_enterprise import settings
from wechatpy.enterprise import parse_message, create_reply

from gptbase_enterprise.models import WechatMessageLog
from gptbase_enterprise.settings import GPTBASE_KEY, GPTBASE_URL, GPTBASE_AI_ID

router = APIRouter(prefix='/api/v1/wechat', tags=['Wechat'])


# 企业微信验证类
@router.get('/msg')
async def get_msg(msg_signature: str, timestamp: str, nonce: str, echostr: Optional[str] = ''):
    print(f'get_msg_input: {msg_signature}, {timestamp}, {nonce}, {echostr}')
    print(f'get_msg_setting: {settings.WECHAT_TOKEN}, {settings.WECHAT_KEY}, {settings.WECHAT_CORP_ID}')
    crypto = WeChatCrypto(settings.WECHAT_TOKEN, settings.WECHAT_KEY, settings.WECHAT_CORP_ID)
    try:
        echo_str = crypto.check_signature(
            msg_signature,
            timestamp,
            nonce,
            echostr
        )
        print(f'get_msg_success_output: {echo_str}')
        return int(echo_str)
    except InvalidSignatureException as e:
        print(f'get_msg_error_output: {e.errmsg}')
        return 'InvalidSignatureException'


@router.post('/msg')
async def post_msg(msg_signature: str, timestamp: str, nonce: str, request: Request):
    crypto = WeChatCrypto(settings.WECHAT_TOKEN, settings.WECHAT_KEY, settings.WECHAT_CORP_ID)
    raw_message = await request.body()
    try:
        decrypted_xml = crypto.decrypt_message(
            raw_message,
            msg_signature,
            timestamp,
            nonce
        )
    except (InvalidSignatureException, InvalidCorpIdException) as e:
        print(f'post_msg_error_output: InvalidSignatureException or InvalidCorpIdException {e.errmsg}')
        raise
    else:
        msg = parse_message(decrypted_xml)
        new_msg = await WechatMessageLog.create(
            raw_message=raw_message.decode('utf-8'),
            message_type=msg.type,
            decrypted_xml=decrypted_xml,
            msg_type=msg.type,
            answer=msg.content,
            message_msg_id=msg.id,
            message_content=msg.content,
            message_from_user_name=msg.source,
            message_to_user_name=msg.target,
            message_create_time=msg.create_time,
            reply='',
        )
        asyncio_task = asyncio.create_task(_send(msg, new_msg, msg.source))

    return


async def _send(msg, new_msg, user_name):
    req_content = 'System error. Please try again later.'
    if msg.type == "text":
        print(f'Sending to gptbase: {msg.content} session_id: {msg.source}_{msg.target}_{new_msg.id}')
        start_time = datetime.now()
        gptbase_message_info = await _send_gptbase_message(msg.content,
                                                           f'{msg.source}_{msg.target}_{new_msg.id}')
        end_time = datetime.now()
        time_delta = (end_time - start_time).total_seconds()
        print(f'gptbase tims: {time_delta}')
        print(f'Receive gptbase return message: {gptbase_message_info}')
        if gptbase_message_info and gptbase_message_info.get('messages') is None:
            req_content = gptbase_message_info.get('answer')
            await WechatMessageLog.filter(id=new_msg.id).update(reply=gptbase_message_info.get('answer'),
                                                                reply_create_time=datetime.now())
        else:
            print(f'gptbase_message_info_error: {gptbase_message_info.get("messages")}')
            req_content = f'system error: {gptbase_message_info.get("messages")}'
            await WechatMessageLog.filter(id=new_msg.id).update(reply_error_msg=gptbase_message_info.get("messages")
                                                                , reply_create_time=datetime.now())
    else:
        req_content = 'Except for text messages, others are not supported yet.'

    # 主动发送消息
    wechat_client = WeChatClient(
        settings.WECHAT_CORP_ID,
        settings.WECHAT_SECRET,
    )
    msg_info = wechat_client.message.send_markdown(agent_id=settings.WECHAT_AGENT_ID, user_ids=f'{user_name}',
                                                   content=req_content)
    print(f'Actively send message results: {msg_info}')


async def _send_gptbase_message(question: str, session_id: str):
    print(f'_send_gptbase_message: Start')
    headers = {"Authorization": f"Bearer {GPTBASE_KEY}"}
    timeout = httpx.Timeout(600.0, read=600.0)
    body = {
        'ai_id': GPTBASE_AI_ID,
        'session_id': session_id,
        'question': question,
        'stream': False,
        'format': 'JSON_AST'
    }
    body_str = json.dumps(body)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.request('POST', f'{GPTBASE_URL}/questions/{GPTBASE_AI_ID}',
                                            data=body_str,
                                            headers=headers)
            if response.status_code != 200:
                detail = response.json().get('detail') if response.content else None
                raise HTTPException(
                    status_code=response.status_code, detail=detail
                )
            if response.content:
                return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[gptbase_error]: {e}")
            raise e
        except Exception as e:
            print(f"[gptbase_error]: {e}")
            raise e
