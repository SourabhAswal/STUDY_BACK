from rest_framework import viewsets
from rest_framework.response import Response
import hashlib
from rest_framework import status
from rest_framework import response
from google.cloud import storage
# from empregapi import settings
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.decorators import action

from .serializers import MessageSerializer, \
    GroupSerializer, MembersSerializer, EventSerializer, \
    GroupjsonSerializer
from .models import Message, Group, Members
from userauthn.serializers import User, UserSerializer
from Studygroup_SuperAdmin.models import Roles
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
import json
import django.core.serializers
import django.http
import logging
import traceback
import datetime

bigBlueButtonURL = "https://mybbb.realcoderz.com/bigbluebutton/api/"
secret = "iTR2xOwzBfSqIT64R4BKbd5SD1WmtI628aQ3ccg8Po"

logger = logging.getLogger('django')


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         user = User.objects.all().order_by('id')
#         logger.info(' >> FETCHING THE USER DATA  << ')
#         return user


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        message = Message.objects.all().order_by('id')
        logger.info(' >> FETCHING THE Message DATA  << ')
        return message


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        print("heloooo")

        group = Group.objects.all()
        serializer = GroupSerializer(data=request.data)
        print(serializer)
        id = request.data['userId']
        users = User.objects.filter(id=id)
        icon = request.data.get('imagess')
        # userid=User.objects.get(id=id)
        if serializer.is_valid():
            icon_url = upload_icon_blob(settings.GOOGLE_CLOUD_STORAGE_BUCKET, icon, "iconcontent/"+icon.name)
            groupss = Group.objects.create(
                gpName=request.data['gpName'], link=request.data['link'], description=request.data['description'], imagess=settings.GOOGLE_CLOUD_STORAGE_URL+"iconcontent/"+icon.name)
            # goups.save()
            groupss.userId.add(*users)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Group created successfully',
            }
            return Response(response, status=status_code)
        return Response({"error": "Please provide all fields"})

    def get_queryset(self):
        group = Group.objects.all().order_by('id')
        print(group)
        logger.info(' >> FETCHING THE GROUP DATA  << ')
        return group


class GroupjsonViewSet(viewsets.ModelViewSet):
    serializer_class = GroupjsonSerializer

    def get_queryset(self):
        group = Group.objects.all().order_by('id')
        print("ak")
        print(group)
        # print(group.imagess)
        logger.info(' >> FETCHING THE GROUPJOSN DATA  <<')
        return group


class MembersViewSet(viewsets.ModelViewSet):
    serializer_class = MembersSerializer

    def get_queryset(self):
        member = Members.objects.all().order_by('id')
        logger.info(' >> FETCHING THE MEMBER DATA  << ')
        return member

    def create(self, request, *args, **kwargs):
        data = request.data
        gpId = Group.objects.get(id=data['grp_ID'])
        userId = User.objects.get(id=data['user_ID'])

        id = data['grp_ID']
        id = str(id)
        # name = data["full_name"]
        logger.info(' >> Create a unique link for specific user << ')

        ##########################  User LINK #########################################

        joinMeeting = "fullName=" + userId.username + "&meetingID=" + \
            "bootcamp" + id + "&password=" + "attendee" + "&redirect=true"
        convert = "join" + joinMeeting + secret
        hashcode = hashlib.sha256(convert.encode()).hexdigest()
        attendeUrl = bigBlueButtonURL + "join?" + joinMeeting + "&checksum=" + hashcode

        logger.info(' >> Create a unique link for Group Admin << ')

        joinMeeting = "fullName=" + userId.username + "&meetingID=" + \
            "bootcamp" + id + "&password=" + "moderator" + "&redirect=true"
        convert = "join" + joinMeeting + secret
        hashcode = hashlib.sha256(convert.encode()).hexdigest()
        adminUrl = bigBlueButtonURL + "join?" + joinMeeting + "&checksum=" + hashcode

        query_results = Members.objects.create(grp_ID=gpId, user_ID=userId)
        query_results.grp_Id = gpId
        query_results.user_ID = userId
        query_results.gpName = gpId.gpName
        query_results.userURL = attendeUrl
        query_results.adminURL = adminUrl
        query_results.full_name = str(userId.username)
        logger.info(' >> Save the data into database << ')

        query_results.save()

        serializer = MembersSerializer(query_results)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        member = Members.objects.all().order_by('id')
        return member


# class RightViewSet(viewsets.ModelViewSet):
#     serializer_class = RightSerializer
#
#     def get_queryset(self):
#         student = Right.objects.all()
#         return student
#
#     def create(self, request, *args, **kwargs):
#         # bigBlueButtonURL = "https://mybbb.realcoderz.com/bigbluebutton/api/"
#         #
#         # secret = "iTR2xOwzBfSqIT64R4BKbd5SD1WmtI628aQ3ccg8Po"
#
#         data = request.data
#         # print(data["role_Id"])
#         new_student = Right.objects.create()
#
#
#         new_student.save()
#
#         for user in data["user_ID"]:
#             # print(user["id"])
#             user_obj = User.objects.get(id=user["id"])
#             new_student.user_ID.add(user_obj)
#
#         # print(Group.objects.get(id=31))
#
#         for module in data["role_Id"]:
#             module_obj = Role.objects.get(id=module["id"])
#             new_student.role_Id.add(module_obj)
#
#         serializer = RightSerializer(new_student)
#         return Response(serializer.data)
#
#
# class RoleViewSet(viewsets.ModelViewSet):
#     serializer_class = RoleSerializer
#
#     def get_queryset(self):
#         module = Role.objects.all()
#         logger.info(' >> fetch the role details << ')
#         return module
#
#
# class RoleJsonViewSet(viewsets.ModelViewSet):
#     serializer_class = RoleJsonSerializer
#
#     def get_queryset(self):
#         module = Role.objects.all()
#         return module
#
#
# class BigBlueButtonViewSet(viewsets.ModelViewSet):
#     serializer_class = BigBlueButtonSerializer
#
#     def get_queryset(self):
#         url = BigBlueButton.objects.all()
#         logger.info(' >> Check the request for specific group << ')
#         return url
#
#     def create(self, request, *args, **kwargs):
#         bigBlueButtonURL = "https://mybbb.realcoderz.com/bigbluebutton/api/"
#         secret = "iTR2xOwzBfSqIT64R4BKbd5SD1WmtI628aQ3ccg8Po"
#
#         data = request.data
#         gpId = Group.objects.get(id=data['gpId'])
#
#         # Role Model Testing
#
#         # Right Model Testing
#
#         id = data['gpId']
#
#         logger.info(' >> Creating the link for a particular group << ')
#
#         # Create Meeting #
#
#         #      "&logoutURL=localhost:3000/UserDashboard"
#         createMeeting = "name=" + gpId.gpName + "&logoutURL=localhost:3000/UserDashboard" + "&meetingID=bootcamp" + str(
#             id) + "&moderatorPW=moderator" + "&attendeePW=attendee"
#         convert = "create" + createMeeting + secret
#         hashcode = hashlib.sha256(convert.encode()).hexdigest()
#         createMeeting = bigBlueButtonURL + "create?" + createMeeting + "&checksum=" + hashcode
#         logger.info(' >> Creating the link for a User << ')
#
#         #  User LINK #
#         id = str(id)
#         joinMeeting = "fullName=VAIBHAV" + id + "&meetingID=" + "bootcamp" + id + "&password=" + "attendee" + "&redirect=true";
#         convert = "join" + joinMeeting + secret
#         hashcode = hashlib.sha256(convert.encode()).hexdigest()
#         attendeUrl = bigBlueButtonURL + "join?" + joinMeeting + "&checksum=" + hashcode
#
#         ##  ADMIN LINK #
#
#         logger.info(' >> Creating the link for a ADMIN << ')
#         joinMeeting = "fullName=SUMIT" + id + "&meetingID=" + "bootcamp" + id + "&password=" + "moderator" + "&redirect=true";
#         convert = "join" + joinMeeting + secret
#         hashcode = hashlib.sha256(convert.encode()).hexdigest()
#         adminUrl = bigBlueButtonURL + "join?" + joinMeeting + "&checksum=" + hashcode
#
#         query_results = BigBlueButton.objects.create(gpId=gpId)
#         query_results.gpId = gpId
#         query_results.createLink = createMeeting
#         query_results.meetingUserUrl = attendeUrl
#         query_results.meetingAdminUrl = adminUrl
#         logger.info(' >> Post a big blue button data << ')
#
#         query_results.save()
#         serializer = BigBlueButtonSerializer(query_results)
#         return Response(serializer.data)


# class GraphViewSet(viewsets.ModelViewSet):
#     # serializer_class = RoleJsonSerializer
#
#     def get_queryset(self):
#         data =list(Role.objects.values())
#         return JsonResponse(data, safe=False)
#
#
# def get_graph(request):
#     # fetch date and time
#     member = Group.objects.all()
#     logger.info(' >> Fetching the data for graph << ')
#
#     arr = []
#
#     for mem in member:
#         user = Member.objects.filter(grp_ID=mem.id)
#         message = Message.objects.filter(grp_ID=mem.id)
#         arr.append({
#             'group': mem.gpName,
#             'user': len(user),
#             'message': len(message)
#         })
#
#     # print(json.dumps(arr))
#
#     return HttpResponse(json.dumps(arr))
#
#
def get_group(request, user):
    a = 1
    member = Members.objects.filter(user_ID=user)
    user = member
    post_list = serializers.serialize('json', member)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


def userLogin(request, username, password):
    try:
        user = list(User.objects.filter(
            username=username, password=password).values())
        print(user)
        if len(user) == 0:
            logger.warn("User Login fail for ", user)

    except Exception as e:
        logger.error("Error occur while sending a email error =", e)

    return JsonResponse(user, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def messageFunctionality(request):
    if request.method == "DELETE":
        id = request.data['id']
        msg = Message.objects.filter(id=id).delete()
        return HttpResponse("", content_type="text/json-comment-filtered")


# @api_view(['GET', 'POST', 'DELETE'])
# def deleteGroup(request):
#     if request.method == "POST":
#         id = request.data['id']
#         grp = Group.objects.filter(id=id).delete()
#         return HttpResponse("", content_type="text/json-comment-filtered")
#
#
# @api_view(['GET', 'POST', 'DELETE'])
# def deleteUser(request):
#     if request.method == "POST":
#         id = request.data['id']
#         user = User.objects.filter(id=id).delete()
#         print('user = ', user)
#         return HttpResponse("", content_type="text/json-comment-filtered")
#

@api_view(['GET', 'POST', 'DELETE'])
def leaveGroup(request):
    if request.method == "POST":
        try:
            id = request.data['id']
            member = Members.objects.filter(id=id).delete()

            logger.info("Delete Successfully for member id ", id)
            return HttpResponse("Delete Successfully", content_type="text/json-comment-filtered")
        except Exception as e:
            logger.error("Error while deleting the member")


@api_view(['GET', 'POST', 'DELETE'])
def userById(request, method):
    print("userby id")

    print(request.data)
    if method == "get":
        id = request.data['id']
        print(id)
        user = list(User.objects.filter(id=id).values())
        print(user)
        return HttpResponse(user, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def groupById(request, method):
    print(request.data)
    if method == "get":
        id = request.data['id']
        print(id)
        user = list(Group.objects.filter(id=id).values())
        user = list(User.objects.filter(id=id).values())
        response = {}
        response = serializers.serialize("json", Group.objects.filter(id=id))
        return HttpResponse(response, content_type="application/json")


#  Email
@api_view(['GET', 'POST', 'DELETE'])
def send_email_api(request):
    try:
        send_email_from_app(request)
        data = {
            'success': True,

            'message': 'Email sent successfully'

        }
    except Exception as e:

        logger.error("Error occur while sending a email error =", e)
        data = {
            'success': False,

            'message': 'Email not sent,Please Check Your Email'

        }

    return JsonResponse(data)


def send_email_from_app(request):
    print(request.data)
    data = request.data
    email = data['email']
    print(email)
    subject = data['subject']
    message = data['message']
    email = email.split(',')

    if len(email) != 1:
        email.pop()
    html_tpl_path = 'email_templates/welcome.html'
    context_data = {'name': 'JK'}
    # email_html_template = get_template(html_tpl_path).render(context_data)
    receiver_email = email
    # print(receiver_email)
    email_msg = EmailMessage(subject,
                             "<p> Dear Candidate</p>"
                             "<h4>" + message + "</h4>",
                             settings.APPLICATION_EMAIL,
                             receiver_email,
                             reply_to=[settings.APPLICATION_EMAIL]
                             )
    # this is the crucial part that sends email as html content but not as a plain text
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)


# @api_view(['GET', 'POST', 'DELETE', 'PUT'])
# def super_Admin(request):
#     try:
#         user = request.data['email']
#         email = request.data['email']
#         password = request.data['password']
#         user = list(User.objects.filter(email=user, password=password).values())
#
#         if len(user) == 0:
#             logger.error("This user id is not exit for " + email)
#     except Exception as e:
#         logger.error("Error", e)
#
#     if len(user) > 0:
#         role = Role.objects.filter(id=5)
#         # User = role[0].user_ID
#
#     return JsonResponse(user, safe=False)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def update_User(request):
    print(request.data)
    data = request.data
    id = data['id']
    try:
        user = User.objects.filter(id=id).update(email=data["email"])
        print(user)
        if user == 1:
            return JsonResponse({"value": 'success'}, safe=False)
        else:
            return JsonResponse({"value": 'error'}, safe=False)
    except Exception as e:
        return JsonResponse({"value": 'error'}, safe=False)


# @api_view(['GET', 'POST', 'DELETE'])
# def pendingRequest(request):
#     print('user', request)
#     user = list(User.objects.filter(approve='No').values())
#     return JsonResponse(user, safe=False)


# class CreateRoleViewSet(viewsets.ModelViewSet):
#     serializer_class = CreateRoleSerializer

#     def get_queryset(self):
#         crole = CreateRole.objects.all().order_by('id')
#         return crole
def upload_icon_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source_file_name.file.read())
    return blob.public_url