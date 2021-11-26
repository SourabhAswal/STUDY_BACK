from django.db import models

# Create your models here.
from django.db import models
from django.db.models import CASCADE
import logging, traceback

logger = logging.getLogger('django')
# Create your models here.
from Studygroup_User.models import Group,Members,Message
from userauthn.serializers import User
class Roles(models.Model):
    # mid = models.AutoField(primary_key=True, max_length=20)
    role_name = models.CharField(max_length=50, unique=True)
    role_type = models.CharField(max_length=300, default=True)
    role_des = models.CharField(max_length=300, default=True)
    user_ID = models.ManyToManyField(User,blank=True)
    # img = models.TextField(null=True)

    logger.info(' >> CREATING THE ROLE FIELD << ')

    def __str__(self):
        return self.role_name


class Right(models.Model):
    user_ID = models.ManyToManyField(User)
    role_Id = models.ManyToManyField(Roles)
    logger.info(' >> CREATING THE Right  << ')

class BigBlueButton(models.Model):
    gpId = models.ForeignKey(Group, on_delete=CASCADE)
    createLink = models.CharField(max_length=300, default=True)
    meetingAdminUrl = models.CharField(max_length=300, default=True)
    meetingUserUrl = models.CharField(max_length=300, default=True)
    logger.info(' >> CREATING THE Big Blue Button Field  << ')
