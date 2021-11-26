import logging
import traceback
from codecs import Codec

from rest_framework import serializers
from .models import  Message, Group, Members
from userauthn.serializers import User
logger = logging.getLogger('django')

#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'full_name','avatar', 'email', 'date', 'password','imgs')
#         logger.info(' >> JSON DATA OF USER  << ')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 'gpName','date1','dateTime', 'emailSend',   'meet', 'subscribe', 'role', 'link', 'description',
            'imagess', 'topic','userId',  'createdBy','imgs')
        logger.info(' >> JSON DATA OF GROUP  << ')
        # depth = 2



class GroupjsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 'gpName', 'date1', 'dateTime', 'emailSend', 'meet', 'subscribe', 'role', 'link', 'description',
            'imagess', 'topic', 'userId', 'createdBy', 'imgs')

        depth = 2


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'grp_ID', 'user', 'group', 'messages', 'images', 'files','img','createdBy')
        logger.info(' >> JSON DATA OF MESSAGE  << ')


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ('id', 'grp_ID', 'user_ID', 'role', 'gpName', 'photo', 'full_name', 'userURL', 'adminURL','createdBy')
        logger.info(' >> JSON DATA OF MEMBER  << ')
    # depth = 2


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ('id', 'grp_ID', 'user_ID', 'role', 'gpName', 'photo', 'full_name', 'userURL', 'adminURL')
        depth = 1
#
#
# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['id', 'role_name', 'role_type','role_des', 'user_ID']
#         logger.info(' >> JSON DATA OF ROLE  << ')
#
#
# class RoleJsonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['id', 'role_name', 'role_type','role_des', 'user_ID']
#         depth = 2
#
#
# class RightSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Right
#         fields = ['id', 'role_Id', 'user_ID']
#         # depth = 2
#         logger.info(' >> JSON DATA OF RIGHT << ')
#
#
# class BigBlueButtonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BigBlueButton
#         fields = ['id', 'gpId', 'createLink', 'meetingAdminUrl', 'meetingUserUrl']
#         logger.info(' >> JSON DATA OF BIGBLUEBUTTON  << ')


# class CreateRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CreateRole
#         fields=['id','role_name','role_type','role_des','user_ID']
#         logger.info('>> JSON DATA OF CREATEROLE')


