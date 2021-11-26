import logging
import traceback
from codecs import Codec

from rest_framework import serializers
from .models import  Right, Roles, BigBlueButton

logger = logging.getLogger('django')

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'role_name', 'role_type','role_des', 'user_ID']
        logger.info(' >> JSON DATA OF ROLE  << ')


class RoleJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'role_name', 'role_type','role_des', 'user_ID']
        depth = 2


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = ['id', 'role_Id', 'user_ID']
        # depth = 2
        logger.info(' >> JSON DATA OF RIGHT << ')


class BigBlueButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BigBlueButton
        fields = ['id', 'gpId', 'createLink', 'meetingAdminUrl', 'meetingUserUrl']
        logger.info(' >> JSON DATA OF BIGBLUEBUTTON  << ')
