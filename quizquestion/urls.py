from django.urls import path
from .views import savequestion
from quizquestion import views
urlpatterns = [
    path('', views.savequestion,name='question'),
    path('bulkupload', views.submitquestion,name='bulkupload'),
]