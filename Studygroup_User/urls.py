from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import  MessageViewSet, GroupViewSet, MembersViewSet, EventViewSet , \
    GroupjsonViewSet,    get_group, userLogin, \
    messageFunctionality, leaveGroup, userById, send_email_api,groupById,update_User

# from .views import geeks_view

router = routers.DefaultRouter()
# router.register(r'user', UserViewSet, basename="user")
router.register(r'message', MessageViewSet, basename="message")
router.register(r'group', GroupViewSet, basename="group")
router.register(r'groupjson', GroupjsonViewSet, basename="groupjson")
router.register(r'member', MembersViewSet, basename="member")
router.register(r'event', EventViewSet, basename="event")
# router.register(r'right', RightViewSet, basename="right")
# router.register(r'role', RoleViewSet, basename="role")
# router.register(r'rolejson', RoleJsonViewSet, basename="rolejson")
# router.register(r'meetingLink', BigBlueButtonViewSet, basename="meetingLink")
# router.register(r'createrole',CreateRoleViewSet,basename="createrole")


# router.register(r'get_graph', contact, basename="about")
app_name = 'Studygroup_User'


urlpatterns = [
    # path('graph', get_graph),
    path('login/<username>/<password>', userLogin),
    path('groupDetails/<user>', get_group),
    path('msgfunc', messageFunctionality),
    path('leaveGroup', leaveGroup),
    # path('deleteGroup', deleteGroup),
    # path('deleteUser', deleteUser),
    path('userById/<method>', userById),
    path('groupById/<method>', groupById),
    path('sendemail/', send_email_api),
    # path('superAdmin',super_Admin),
    path('updatesUser', update_User),
    # path('pendingRequest', pendingRequest),
    # path('getRole',get_role),

    path('', include(router.urls)),
]
