from django.urls import path
from .views import SetNewPasswordAPI, PasswordTokenCheckAPI, RegisterView, UserLoginView, SendOTP, RecoverPassword
from django.urls.resolvers import URLPattern
from .views import RegisterView, UserLoginView, SendOTP, editUser, showUser, updateRole
from userauthn import views

from .views import RegisterView, UserLoginView, SendOTP
from django.urls.resolvers import URLPattern
from .views import SetNewPasswordAPI, PasswordTokenCheckAPI, RegisterView, UserLoginView, SendOTP, RecoverPassword, UserList, deleteUser, UserDetails

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('signin/', UserLoginView.as_view()),
    path('sendotp/', SendOTP.as_view()),
    path('recoverPassword/', RecoverPassword.as_view(), name='recoverPassword'),
    path('password-reset-confirm/<userIdB64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPI.as_view(),
         name='password-reset-complete'),
    path('edit/', editUser),
    path('show/<str:userid>', showUser),

    path('allusers/', UserList.as_view(), name='allusers'),
    path('userdetails/<str:pk>', UserDetails.as_view(), name='userdetails'),
    path('updaterole/<str:pk>', updateRole, name='updaterole'),
    path('deleteuser/<str:pk>', deleteUser, name='deleteuser'),
]
