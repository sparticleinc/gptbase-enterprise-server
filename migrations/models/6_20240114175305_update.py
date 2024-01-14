from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "wechatmessagelog" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "raw_message" TEXT NOT NULL,
    "decrypted_xml" TEXT NOT NULL,
    "message_type" VARCHAR(255) NOT NULL,
    "message_content" TEXT NOT NULL,
    "message_msg_id" VARCHAR(255) NOT NULL,
    "message_from_user_name" VARCHAR(255) NOT NULL,
    "message_to_user_name" VARCHAR(255) NOT NULL,
    "answer" TEXT
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "wechatmessagelog";"""
