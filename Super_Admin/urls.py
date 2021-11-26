from django.urls import path
from .views import RoleCreateApi, RoleDetail, AllRole, RoleUpdate, SignupRole, editRole, deleteRole, updateInitialRole


app_name = 'Super_Admin'

urlpatterns = [
    path('create/', RoleCreateApi.as_view(), name='rolelist'),
    path('list/<int:pk>/', RoleDetail.as_view(), name='roledetail'),
    path('allroles/', AllRole.as_view(), name='allroles'),
    path('mapping/', RoleUpdate.as_view(), name='mapping'),
    path('signuprole/<int:pk>/', SignupRole.as_view(), name='signuprole'),
    # path('role/<int:pk>/', RoleList.as_view(), name='role'),
    path('editrole/<int:pk>/', editRole, name='editrole'),
    path('deleterole/<int:pk>/', deleteRole, name='deleterole'),
]
