from django.db import models
from django.db.models import CASCADE
import logging, traceback
import datetime
from userauthn.serializers import User
logger = logging.getLogger('django')

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     full_name = models.CharField(max_length=200)
#     avatar = models.ImageField(blank=True, default="images/user.png", null=True, upload_to="images/")
#     approve = models.CharField(max_length=200, default="No")
#     email = models.CharField(max_length=100, unique=True)
#     date = models.DateTimeField(auto_now_add=True)
#     password = models.CharField(max_length=20)
#     imgs = models.TextField(null=True)
#
#     logger.info(' >> CREATING THE USER FIELD <<  ')
#
#     def __str__(self):
#         return self.username


class Group(models.Model):
    gpName = models.CharField(max_length=100, unique=True, default='Java')
    date1 = models.CharField(max_length=100, default='06/03/2021 18:00')
    emailSend = models.CharField(max_length=10, default='No')
    dateTime =models.DateTimeField(null=True, blank=True)
    meet = models.CharField(max_length=300, null=True)
    subscribe = models.CharField(max_length=100, default='okay')
    role = models.CharField(max_length=100, default='user')
    link = models.CharField(max_length=100, default='https://en.wikipedia.org/wiki/Main_Page')
    description = models.CharField(max_length=1000, default=' Enter some description')
    imagess = models.TextField(default="images/group.png", null=True,blank=True,max_length=200)
    # user_Id = models.ForeignKey(User, on_delete=CASCADE ,default =1)
    topic = models.CharField(max_length=100, default='topic')
    userId = models.ManyToManyField(User)
    createdBy = models.DateTimeField(auto_now_add=True)
    imgs = models.TextField(null=True)

    logger.info(' >> CREATING THE GROUP  FIELD<< ')

    def __str__(self):
        return self.gpName


class Members(models.Model):
    grp_ID = models.ForeignKey(Group, on_delete=CASCADE)
    user_ID = models.ForeignKey(User, on_delete=CASCADE)
    full_name = models.CharField(max_length=200, default="abc")
    role = models.CharField(max_length=100, default="user")
    gpName = models.CharField(max_length=100, default="Java")
    photo = models.ImageField(default="images/group.png", blank=True, null=True, upload_to="images/")
    userURL = models.CharField(max_length=300, default="user")
    adminURL = models.CharField(max_length=300, default="admin")
    createdBy = models.DateTimeField(auto_now_add=True)
    logger.info(' >> CREATING THE  MEMBER  FIELD << ')

    def nameFile(instance, filename):
        return '/'.join(['images', str(instance.name), filename])


class Message(models.Model):
    grp_ID = models.ForeignKey(Group, on_delete=CASCADE)
    user = models.CharField(max_length=100, default='manager')
    group = models.CharField(max_length=100, default='Java')
    messages = models.TextField(max_length=100, null=True, blank=True)
    images = models.TextField(blank=True, null=True,max_length=200)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    img = models.TextField(null=True)
    createdBy = models.DateTimeField(auto_now_add=True)

    logger.info(' >> CREATING THE MESSAGE field  << ')

    def __str__(self):
        return self.group

#
# class Role(models.Model):
#     # mid = models.AutoField(primary_key=True, max_length=20)
#     role_name = models.CharField(max_length=50, unique=True)
#     role_type = models.CharField(max_length=300, default=True)
#     role_des = models.CharField(max_length=300, default=True)
#     user_ID = models.ManyToManyField(User, blank=True)
#     # img = models.TextField(null=True)
#
#     logger.info(' >> CREATING THE ROLE FIELD << ')
#
#     def __str__(self):
#         return self.role_name
#
#
# class Right(models.Model):
#     user_ID = models.ManyToManyField(User)
#     role_Id = models.ManyToManyField(Role)
#     logger.info(' >> CREATING THE Right  << ')
#
#
# class BigBlueButton(models.Model):
#     gpId = models.ForeignKey(Group, on_delete=CASCADE)
#     createLink = models.CharField(max_length=300, default=True)
#     meetingAdminUrl = models.CharField(max_length=300, default=True)
#     meetingUserUrl = models.CharField(max_length=300, default=True)
#     logger.info(' >> CREATING THE Big Blue Button Field  << ')


# class CreateRole(models.Model):
#     role_name = models.CharField(unique=True, max_length=100)
#     role_type = models.CharField(max_length=300, default=True)
#     role_des = models.CharField(max_length=300, default=True)
#     user_ID = models.ManyToManyField(User, blank=True)


