from django.urls import path, include
from rest_framework import routers

from course.models import UploadPpt, Uploadpdf
from . import views

from .views import CourseSecList, ViewUploadPdfAPI, CourseAllDataAPIView, CourseSubSecList, CourseViewSet,MemberViewSet, UploadPdf,UploadPptAPIView,enroll_course,unenroll,UploadSubVideoAPIView,Check_courseVisited,getSubVideoAPIView,GetPptAPIView, UploadExternalVideoAPIView, defaultsubIDAPIView

from django.contrib import admin
# from django.http import HttpResponse

router = routers.DefaultRouter()
router.register(r'course',CourseViewSet,basename="course")
router.register(r'members',MemberViewSet,basename="member")
app_name = 'course'


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('enroll_course',enroll_course),
    path('unenroll/',unenroll),

    #courseSec urls
    path('courseSec-list/<str:pk>', views.courseSecList, name="courseSec-list"),
	path('courseSec-create/', views.courseSecCreate, name="courseSec-create"),
    path('courseSec-update/<str:pk>/', views.courseSecUpdate, name="courseSec-update"),
	path('courseSec-delete/<str:pk>/', views.courseSecDelete, name="courseSec-delete"),
    path('courseSec-list/',CourseSecList.as_view()),
    #courseSubSec urls
    path('courseSubSec-list/<str:pk>', views.courseSubSecList, name="courseSubSec-list"),
	path('courseSubSec-create/', views.courseSubSecCreate, name="courseSubSec-create"),
    path('courseSubSec-update/<str:pk>/', views.courseSubSecUpdate, name="courseSubSec-update"),
	path('courseSubSec-delete/<str:pk>/', views.courseSubSecDelete, name="courseSubSec-delete"),
    path('courseSubSec-list/',CourseSubSecList.as_view()),

    #upload pdf urls
    path('upload-ppt/', UploadPptAPIView.as_view()),
    path('upload-ppt/<str:pk>/',UploadPptAPIView.as_view()),
    # path('upload-ppt/<str:id>/',UploadPptAPIView.as_view()),

    #upload presentation urls
    path('upload-pdf/', UploadPdf.as_view()),
    path('upload-pdf/<str:pk>/',UploadPdf.as_view()),
    path('upload-pdf-list/<str:pk>/',UploadPdf.as_view()),
    path('viewPdf/<str:pk>/', ViewUploadPdfAPI.as_view()),
    path('get-ppt/<str:pk>/', GetPptAPIView.as_view()),

    path('viewAllContent/<str:pk>/', CourseAllDataAPIView.as_view()),

    #upload subsectionvideo urls
    path('upload-subVideo/', UploadSubVideoAPIView.as_view()),
    path('upload-subVideo/<str:pk>/', UploadSubVideoAPIView.as_view()),
    path('user/<userId>/courseVisited/<courseId>/', Check_courseVisited.as_view()),
    path('get-subVideo/<str:pk>/', getSubVideoAPIView.as_view()),

    #Default Sub Section Id
    path('post-defaultSubId/',defaultsubIDAPIView.as_view()),
    path('post-defaultSubId/<str:pk>/',defaultsubIDAPIView.as_view()),


    path('upload-extVideo/', UploadExternalVideoAPIView.as_view()),
    path('upload-extVideo/<str:pk>/', UploadExternalVideoAPIView.as_view()),

]
