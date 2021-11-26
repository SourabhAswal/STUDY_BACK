from django.db.models import query
from rest_framework import generics
from Super_Admin.models import Role
from .serializers import RoleSerializer
from rest_framework.response import Response
from rest_framework import status

from Super_Admin import serializers

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
import requests
from rest_framework.decorators import api_view
import urllib

from .models import Role

User = get_user_model()


class RoleCreateApi(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# class RoleList(generics.GenericAPIView):
#     serializer_class = RoleSerializer
#     queryset = Role.objects.all()

#     def get(self, request, pk):
#         self.queryset = Role.objects.all().filter(
#             role_name=request['role_name'])
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)


class RoleDetail(generics.GenericAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def get(self, request, pk):
        self.queryset = Role.objects.all().filter(user_id=pk)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class AllRole(generics.GenericAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def get(self, request):
        self.queryset = Role.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class RoleUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            li = []
            li.append(request.data['Admin'])
            li.append(request.data['Instructor'])
            li.append(request.data['Student'])
            ind = 0
            roles = Role.objects.all()
            for role in roles:
                s = li[ind].split(',')
                ind += 1
                role.user_id.clear()
                for n in s:
                    user = User.objects.get(username=n)
                    role.user_id.add(user)
                role.save()

            status_code = status.HTTP_200_OK
            message = 'Role updated successfully'
            success = 'True'
        except:
            success = 'False'
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = 'Some error occured'
        response = {
            'success': success,
            'status code': status_code,
            'message': message,
        }
        return Response(response, status=status_code)

    def perform_update(self, serializer):
        serializer.save(updated_by_user=self.request.user)


@api_view(['PUT'])
def updateInitialRole(request, pk):
    try:
        role = Role.objects.get(id=pk)
        user = User.objects.get(id=request.data['user_id'])
        role.user_is.add(user)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Role updated successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Some error occured'
        }
    return Response(response, status=status_code)


@api_view(['PUT'])
def editRole(request, pk):
    try:
        Role.objects.filter(id=pk).update(role_name=request.data['role_name'])
        Role.objects.filter(id=pk).update(role_type=request.data['role_type'])
        Role.objects.filter(id=pk).update(role_des=request.data['role_des'])
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Role updated successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Some error occured'
        }
    return Response(response, status=status_code)


@api_view(['DELETE'])
def deleteRole(request, pk):
    try:
        role = Role.objects.get(id=pk)
        role.delete()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Role deleted successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Some error occured'
        }
    return Response(response, status=status_code)


class SignupRole(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def put(self, request, pk, *args, **kwargs):
        try:
            role = Role.objects.get(id=pk)
            user = User.objects.get(id=request.data['user_id'])
            role.user_id.add(user)
            role.save()
            status_code = status.HTTP_200_OK
            message = 'Role updated successfully'
            success = 'True'
        except:
            success = 'False'
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = 'Some error occured'
        response = {
            'success': success,
            'status code': status_code,
            'message': message,
        }
        return Response(response, status=status_code)

    def perform_update(self, serializer):
        serializer.save(updated_by_user=self.request.user)


# class RoleMapping(generics.ListCreateAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
        # queryset = Role.objects.all()
        # serializer_class = RoleMappingSerializer

        # def get_queryset(self):
        #     roles = Role.objects.all()
        #     return roles

        # def post(self, request):
        #     # userId = request.data["userId"]
        #     # roleId = request.data["roleId"]
        #     userObj = User.objects.get(id=25)
        #     roleObj = Role.objects.get(id=5)
        #     newRole = Role.objects.create()
        #     newRole.save()
        #     newRole.user_id.add(userObj)
        #     newRole.role_id.add(roleobj)
        #     serializer = RoleMappingSerializer(newRole)
        #     return Response(serialzier.data)


# class RoleViewSet(viewsets.ModelViewSet):
#     serializer_class = RoleSerializer

#     def get_queryset(self):
#         module = Role.objects.all()
#         return module
