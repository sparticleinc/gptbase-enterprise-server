from tortoise import fields, models


class AbstractBaseModel(models.Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Test(AbstractBaseModel):
    name = fields.CharField(max_length=255)

    class Meta:
        table = 'test'
