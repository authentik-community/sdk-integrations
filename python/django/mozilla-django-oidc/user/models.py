from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "oidc_sub"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=150)
    name = models.TextField()
    oidc_sub = models.TextField(unique=True)

    def get_full_name(self):
        return str(self.name).strip()

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return f"{self.name} <{self.email}>"
