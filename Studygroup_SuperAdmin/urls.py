from django.urls import path, include
from rest_framework import routers
from .views import  RightViewSet, RolesViewSet,RoleJsonViewSet, BigBlueButtonViewSet,get_graph,GraphViewSet,pendingRequest,adminPieChart,adminDashboard,deleteUser,deleteGroup,super_Admin,userdetails,updateuserdetails
# from .views import geeks_view

router = routers.DefaultRouter()

router.register(r'role', RolesViewSet, basename="role")
router.register(r'rolejson', RoleJsonViewSet, basename="rolejson")
router.register(r'meetingLink', BigBlueButtonViewSet, basename="meetingLink")
# router.register(r'right', RightViewSet, basename="right")
# router.register(r'createrole',CreateRoleViewSet,basename="createrole")

# router.register(r'get_graph', contact, basename="about")
app_name = 'Studygroup_SuperAdmin'

urlpatterns = [
    path('graph', get_graph),
    path("userdetails",userdetails),
    path("updateuserdetails",updateuserdetails),
    # path('login/<user>/<password>', userLogin),
    # path('groupDetails/<user>', get_group),
    # path('msgfunc', messageFunctionality),
    # path('leaveGroup', leaveGroup),
    path('deleteGroup', deleteGroup),
    path('deleteUser', deleteUser),
    # path('userById/<method>', userById),
    # path('groupById/<method>', groupById),
    # path('sendemail/', send_email_api),
    path('superAdmin',super_Admin),
    # path('updatesUser', update_User),
    path('pendingRequest', pendingRequest),
    # # # path('getRole',get_role),
    path('superAdminDashboard', adminDashboard),
    path('check', adminPieChart),
    path('', include(router.urls)),
]
