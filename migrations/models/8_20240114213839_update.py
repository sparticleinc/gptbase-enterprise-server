from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechatmessagelog" ADD "reply" TEXT;
        ALTER TABLE "wechatmessagelog" ADD "reply_create_time" TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechatmessagelog" DROP COLUMN "reply";
        ALTER TABLE "wechatmessagelog" DROP COLUMN "reply_create_time";"""
