"""SkillBuilder_LMSBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static


from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/' , include('userauthn.urls'),),
    path('', include('course.urls')),
    path('discussion/', include('discussion.urls')),
    path('api/' , include('userauthn.urls'),),
    path('', include('course.urls')),
    path('discussion/', include('discussion.urls')),
    path('question/', include('quizquestion.urls')),
    # path('bulkupload/', include('quizquestion.urls')),
    path('super-admin/', include('Super_Admin.urls', namespace='Super_Admin')),
    path('assignment/', include('assignment.urls')),
    path('', include('Studygroup_User.urls')),
    path('', include('Studygroup_SuperAdmin.urls')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
