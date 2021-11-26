from django.db import models
from course.models import CourseSubSec
from django.db.models import CASCADE

class Assignment(models.Model):
    # assignment_id = models.IntegerField()
    display_name = models.TextField()
    question = models.TextField()
    quesType = models.TextField()
    subsectionid = models.ForeignKey(CourseSubSec, related_name='assignment', on_delete=CASCADE)

    def __str__(self):
        return self.display_name

class AssignmentFile(models.Model):
    userid = models.TextField()
    first_name = models.TextField()
    assignmentFile = models.CharField(blank=True,max_length=200,default='abc')
    subsecid = models.ForeignKey(CourseSubSec,on_delete=models.SET_NULL,blank=True, null=True)
    subsecName = models.TextField()
    secName = models.TextField()
    courseName = models.TextField()

    
