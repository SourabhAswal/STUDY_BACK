from django.db.models import fields
from rest_framework import serializers
from Super_Admin.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role_name', 'role_type', 'role_des']


# class ListRoleSerializer(serializers.Serializer):
#     role_name = serializers.CharField(max_length=255, min_length=4)
#     role_type = serializers.CharField(max_length=255, min_length=4)
#     self_des = serializers.CharField(max_length=255, min_length=4)

#     class Meta:
#         model = Role
#         fields = ['role_name', 'role_type', 'role_des']

#     def validate(self, attrs):
#         print(attrs.get('id'))
#         return({
#             'message': 'hello'
#         })


# class RoleMappingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = '__all__'
