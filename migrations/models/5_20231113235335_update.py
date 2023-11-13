from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "environmentdata" ADD "robot_id" UUID;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "environmentdata" DROP COLUMN "robot_id";"""
