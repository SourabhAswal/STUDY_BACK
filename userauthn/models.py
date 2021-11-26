from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from Super_Admin.models import Role

# Create your models here.
class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=False)
    default_role=models.CharField(max_length=30, null=True)
    role_id = models.ManyToManyField(to=Role, default=3)