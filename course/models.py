

# Create your models here.
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import CASCADE
import logging

from userauthn.serializers import User


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    organization = models.CharField(max_length=100)
    course_start_datetime = models.CharField(max_length=100,default='abc')
    course_end_datetime = models.CharField(max_length=100,default='abc')
    course_des = models.CharField(max_length=200)
    course_img = models.CharField(blank=True,max_length=200,default='abc')
    course_video = models.TextField(null=True)
    course_prerequisite = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.course_name


class CourseSec(models.Model):
    course= models.ForeignKey(Course, related_name='sections', on_delete=CASCADE)
    title= models.TextField(null=True)
    
    def __str__(self):
        return self.title

class CourseSubSec(models.Model):
    courseSub=models.ForeignKey(CourseSec, related_name='subSection', on_delete=CASCADE, null=True) 
    sub= models.TextField(null=True) 
   
    
    def __str__(self):
        return str(self.sub)


class Member(models.Model):
    c_Id = models.ForeignKey(Course, related_name='member',on_delete=CASCADE)
    user=models.ForeignKey(User,related_name='track', on_delete=CASCADE,null=True)
    has_visited=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Uploadpdf(models.Model):
    display_name=models.CharField(max_length=255)
    pdf = models.CharField(max_length=255,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    courseSubSection=models.ForeignKey(CourseSubSec,related_name="pdf",on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.display_name)

class UploadPpt(models.Model):
    display_name = models.CharField(max_length=255)
    ppt = models.CharField(max_length=255, validators=[FileExtensionValidator(allowed_extensions=['ppt'])])
    courseSubSection = models.ForeignKey(CourseSubSec, related_name='ppt', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.display_name)

class UploadSubVideo(models.Model):
    subvideoName = models.CharField(max_length=255)
    subVideo = models.CharField(max_length=255, null=True,validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    courseSubSection = models.ForeignKey(CourseSubSec, related_name='subVideo', on_delete=models.SET_NULL, blank=True, null=True)
    external = models.BooleanField()

    def __str__(self):
        return str(self.subvideoName)
class lastSubsectionVisited(models.Model):
    course_Id = models.ForeignKey(Course, related_name='lastvisitedsub',on_delete=CASCADE,null=True)
    subsection_id = models.CharField(max_length=100)        