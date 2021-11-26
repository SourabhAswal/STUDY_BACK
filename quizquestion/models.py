from django.db import models
from course.models import CourseSubSec
from django.db.models import CASCADE


class QuizQuestion(models.Model):
    coursesubsec_id = models.ForeignKey(
        CourseSubSec, on_delete=CASCADE)
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    answer = models.TextField()
