from django.db import models
from account.models import MyCustomUser
import uuid


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(MyCustomUser, on_delete=models.RESTRICT)

    class Meta:
        abstract = True