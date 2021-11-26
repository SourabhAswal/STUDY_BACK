from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    role_type = models.CharField(max_length=100, default=True)
    role_des = models.CharField(max_length=500, default=True)
    # user_id = models.ManyToManyField(to=settings.AUTH_USER_MODEL, default=1)

    def __str__(self):
        return self.role_name