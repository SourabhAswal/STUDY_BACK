from django.shortcuts import render
from .serializers import RolesSerializer, RightSerializer, RoleJsonSerializer, BigBlueButtonSerializer
from .models import Roles, Right, BigBlueButton
# from main.models import  User,Member,Group,Message
# from Studygroup_User.models import Group
from Studygroup_User.models import  Group, Members, Message
from userauthn.serializers import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response
import hashlib
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
import json
import django.core.serializers
import django.http
import logging, traceback
import datetime

# Create your views here.

bigBlueButtonURL = "https://mybbb.realcoderz.com/bigbluebutton/api/"
secret = "iTR2xOwzBfSqIT64R4BKbd5SD1WmtI628aQ3ccg8Po"

logger = logging.getLogger('django')


class RightViewSet(viewsets.ModelViewSet):
    serializer_class = RightSerializer

    def get_queryset(self):
        student = Right.objects.all()
        return student

    def create(self, request, *args, **kwargs):
        # bigBlueButtonURL = "https://mybbb.realcoderz.com/bigbluebutton/api/"
        #
        # secret = "iTR2xOwzBfSqIT64R4BKbd5SD1WmtI628aQ3ccg8Po"

        data = request.data
        # print(data["role_Id"])
        new_student = Right.objects.create()

        new_student.save()

        for user in data["user_ID"]:
            # print(user["id"])
            user_obj = User.objects.get(id=user["id"])
            new_student.user_ID.add(user_obj)

        # print(Group.objects.get(id=31))

        for module in data["role_Id"]:
            module_obj = Roles.objects.get(id=module["id"])
            new_student.role_Id.add(module_obj)

        serializer = RightSerializer(new_student)
        return Response(serializer.data)


class RolesViewSet(viewsets.ModelViewSet):
    serializer_class = RolesSerializer

    def get_queryset(self):
        module = Roles.objects.all()
        logger.info(' >> fetch the role details << ')
        return module


class RoleJsonViewSet(viewsets.ModelViewSet):
    serializer_class = RoleJsonSerializer

    def get_queryset(self):
        module = Roles.objects.all()
        return module


class BigBlueButtonViewSet(viewsets.ModelViewSet):
    serializer_class = BigBlueButtonSerializer

    def get_queryset(self):
        url = BigBlueButton.objects.all()
        logger.info(' >> Check the request for specific group << ')
        return url

    def create(self, request, *args, **kwargs):
        bigBlueButtonURL = "https://mybbb.realcoderz.com/bigbluebutton/api/"
        secret = "iTR2xOwzBfSqIT64R4BKbd5SD1WmtI628aQ3ccg8Po"

        data = request.data
        gpId = Group.objects.get(id=data['gpId'])

        # Role Model Testing

        # Right Model Testing

        id = data['gpId']

        logger.info(' >> Creating the link for a particular group << ')

        # Create Meeting #

        #      "&logoutURL=localhost:3000/UserDashboard"
        createMeeting = "name=" + gpId.gpName + "&logoutURL=localhost:3000/UserDashboard" + "&meetingID=bootcamp" + str(
            id) + "&moderatorPW=moderator" + "&attendeePW=attendee"
        convert = "create" + createMeeting + secret
        hashcode = hashlib.sha256(convert.encode()).hexdigest()
        createMeeting = bigBlueButtonURL + "create?" + createMeeting + "&checksum=" + hashcode
        logger.info(' >> Creating the link for a User << ')

        #  User LINK #
        id = str(id)
        joinMeeting = "fullName=VAIBHAV" + id + "&meetingID=" + "bootcamp" + id + "&password=" + "attendee" + "&redirect=true";
        convert = "join" + joinMeeting + secret
        hashcode = hashlib.sha256(convert.encode()).hexdigest()
        attendeUrl = bigBlueButtonURL + "join?" + joinMeeting + "&checksum=" + hashcode

        ##  ADMIN LINK #

        logger.info(' >> Creating the link for a ADMIN << ')
        joinMeeting = "fullName=SUMIT" + id + "&meetingID=" + "bootcamp" + id + "&password=" + "moderator" + "&redirect=true";
        convert = "join" + joinMeeting + secret
        hashcode = hashlib.sha256(convert.encode()).hexdigest()
        adminUrl = bigBlueButtonURL + "join?" + joinMeeting + "&checksum=" + hashcode

        query_results = BigBlueButton.objects.create(gpId=gpId)
        query_results.gpId = gpId
        query_results.createLink = createMeeting
        query_results.meetingUserUrl = attendeUrl
        query_results.meetingAdminUrl = adminUrl
        logger.info(' >> Post a big blue button data << ')

        query_results.save()
        serializer = BigBlueButtonSerializer(query_results)
        return Response(serializer.data)


class GraphViewSet(viewsets.ModelViewSet):
    # serializer_class = RoleJsonSerializer

    def get_queryset(self):
        data = list(Roles.objects.values())
        return JsonResponse(data, safe=False)


group = Group.objects.all()


def get_graph(request):
    date = datetime.date.today()
    try:
        user1 = User.objects.filter()
        group = Group.objects.all()
        groupCreated = Group.objects.filter(createdBy=date)
        userCreated = User.objects.filter(date_joined=date)
        # pendingRequest = User.objects.filter(approve='No')
        # print(pendingRequest)
        # print("fb")

        graph = []
        groupData = []
        memberData = []
        messageData = []

        for mem in group:
            user = Members.objects.filter(grp_ID=mem.id)
            message = Message.objects.filter(grp_ID=mem.id)
            groupData.append(mem.gpName)
            memberData.append(len(user))
            messageData.append(len(message))

        graph.append({
            'group': groupData,
            'user': memberData,
            'message': messageData
        })
        # print("thfth")
        card = {
            'user': len(user1),
            'group': len(group),
            # 'request': len(pendingRequest),
            'groupCreated': len(groupCreated),
            'userCreated': len(userCreated)
        }
        # print("thcfj")
        pieChart = adminPieChart()

        dashboard = [{
            'card': card,
            'graph': graph,
            'pieChart': pieChart
        }]
        print("tgj")
        print(dashboard)
        return HttpResponse(json.dumps(dashboard))

    except Exception as e:
        return JsonResponse({"value": e}, safe=False)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def super_Admin(request):
    user=""
    a=""
    try:
        print(request.data)
        email= request.data['username']
        password = request.data['password']
        print(email)
        print(password)
        user = User.objects.filter(email=email)
        print(user)
        if len(user) == 0:
            logger.error("This user id is not exit for " + email)
    except Exception as e:
        print(e)
        # logger.error("Error", e)

    if len(user) > 0:
        role = Roles.objects.filter(id=2)
        user1 = role[0].user_ID
        a=user.all()

    for u in a:
        if user[0]==u:
            value = {
                'status': "true"
            }
            print("vjhcxv")
            return HttpResponse(json.dumps(value))

    value = [{
        'status': "false"
    }]
    print("bdvjhcx")
    return HttpResponse(json.dumps(value))



@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def adminDashboard(request):
    data = request.data
    print(data)
    search = data['search']
    startDate = data['startDate']
    endDate = data['date']

    try:
        total_gp = Group.objects.all()
        total_user = User.objects.all()
        user1 = total_user

        group = total_gp
        print("D")

        if search != '' and startDate != '' and endDate != '':
            print("A")

            group = total_gp.filter(gpName=search, createdBy__range=(startDate, endDate))
        else:
            if search != '':
                print("B")

                group = total_gp.filter(gpName=search)
            if startDate != '' and endDate != '':
                print("C")

                group = total_gp.filter(createdBy__range=(startDate, endDate))
                user1 = total_user.filter(date_joined__range=(startDate, endDate))

        # print("LINE 502", group)

        graph = []
        groupData = []
        memberData = []
        messageData = []

        if startDate != '' and endDate != '':
            for mem in group:
                user = Members.objects.filter(grp_ID=mem.id)
                message = Message.objects.filter(grp_ID=mem.id, createdBy__range=(startDate, endDate))
                groupData.append(mem.gpName)
                memberData.append(len(user))
                messageData.append(len(message))
        else:
            for mem in group:
                user = Members.objects.filter(grp_ID=mem.id)
                message = Message.objects.filter(grp_ID=mem.id)
                groupData.append(mem.gpName)
                memberData.append(len(user))
                messageData.append(len(message))

        graph.append({
            'group': groupData,
            'user': memberData,
            'message': messageData
        })
        card = {
            'user': len(user1),
            'group': len(group)
        }

        dashboard = [{
            'card': card,
            'graph': graph
        }]

        return HttpResponse(json.dumps(dashboard))

    except Exception as e:
        print("error", e)
        return JsonResponse({"value": 'error'}, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def pendingRequest(request):
    print('user', request)
    user = list(User.objects.filter(approve='No').values())
    return JsonResponse(user, safe=False)


def adminPieChart():

    try:
        print("kji")
        adminRole = Roles.objects.filter(id=1)
        print(adminRole)
        userId = adminRole[0].user_ID.all()


        print(userId)
        groupName = []
        adminArray = []
        starray = []
        # starray.append(["User", "Admin"])
        a = []
        a1 = []

        for usAdmin in userId:
            # print(" 535 >>>>>>>>>>" + usAdmin.username)
            adminArray.append(usAdmin.first_name)
            groupName = []

            for gp in group:
                gpAdmin = gp.userId.filter(id=usAdmin.id)
                if len(gpAdmin) > 0:
                    groupName.append(gp.gpName)
            if len(groupName) > 0:
                a1.append(len(groupName))
                a.append(usAdmin.first_name)

        # starray.append()

        print(starray)
        return {"name": a, "noOfGp": a1}
        # return JsonResponse({"Admin": starray}, safe=False)

    except Exception as e:
        print("Kajal")
        return JsonResponse({"value": 'error'}, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def deleteGroup(request):
    if request.method == "POST":
        id = request.data['id']
        grp = Group.objects.filter(id=id).delete()
        return HttpResponse("", content_type="text/json-comment-filtered")


@api_view(['GET', 'POST', 'DELETE'])
def deleteUser(request):
    if request.method == "POST":
        id = request.data['id']
        user = User.objects.filter(id=id).delete()
        print('user = ', user)
        return HttpResponse("", content_type="text/json-comment-filtered")

@api_view(['GET', 'POST', 'PUT','DELETE'])
def userdetails(request):

    userdetails=list(User.objects.all().values("id","first_name","email","username"))
    print(userdetails)
    return HttpResponse(json.dumps(userdetails))

@api_view(['GET', 'POST', 'PUT','DELETE'])
def updateuserdetails(request):
    data=request.data
    print(data)
    id=request.data['id']
    userdetail=list(User.objects.filter(id=id).update(id=id))
    print(userdetail)
    return HttpResponse(json.dumps(userdetail))
