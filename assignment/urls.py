from django.urls import path
from .views import AssignmentAPI, AssignmentEditAPI, AssignmentFileAPI,UsersDataAPI

urlpatterns = [
    path('', AssignmentAPI.as_view()),
    path('edit/<int:pk>', AssignmentEditAPI.as_view()),
    path('Assginmentfile', AssignmentFileAPI.as_view()),
    path('usersdata/',UsersDataAPI.as_view()),

]