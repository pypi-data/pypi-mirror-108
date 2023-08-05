from stonehenge.db import fields, models


class User(models.Model):
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    username = fields.CharField(max_length=127)
