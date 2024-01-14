from datetime import datetime

from tortoise import fields, models


class AbstractBaseModel(models.Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractBaseModelWithDeletedAt(AbstractBaseModel):
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        abstract = True

    async def soft_delete(self):
        self.deleted_at = datetime.now()
        await self.save(update_fields=['deleted_at'])


class Test(AbstractBaseModel):
    name = fields.CharField(max_length=255)

    class Meta:
        table = 'test'


# 环境配置
class EnvironmentData(AbstractBaseModelWithDeletedAt):
    name = fields.CharField(max_length=255)
    description = fields.CharField(null=True, max_length=255)
    sort = fields.IntField(null=True)
    data = fields.JSONField(null=True)
    robot_id = fields.UUIDField(null=True)

    class PydanticMeta:
        exclude = (
            'updated_at',
            'deleted_at',
        )


class Config(AbstractBaseModelWithDeletedAt):
    name = fields.CharField(max_length=255)
    description = fields.CharField(null=True, max_length=255)
    data = fields.JSONField(null=True)

    class PydanticMeta:
        exclude = (
            'updated_at',
            'deleted_at',
        )


class WechatMessageLog(AbstractBaseModelWithDeletedAt):
    raw_message = fields.TextField()
    decrypted_xml = fields.TextField()
    message_type = fields.CharField(max_length=255)
    message_content = fields.TextField()
    message_msg_id = fields.CharField(max_length=255)
    message_from_user_name = fields.CharField(max_length=255)
    message_to_user_name = fields.CharField(max_length=255)
    message_create_time = fields.DatetimeField(null=True)
    answer = fields.TextField(null=True)
    reply = fields.TextField(null=True)

    class PydanticMeta:
        exclude = (
            'updated_at',
            'deleted_at',
        )