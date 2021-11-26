from django.db import models
from django.db.models.deletion import CASCADE
from course.models import Course
from userauthn.serializers import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core import serializers


class DiscussionPost(models.Model):
    course = models.ForeignKey(Course, on_delete=CASCADE, null=True)
    name = models.CharField(max_length=80, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True,null=True)
    is_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def save(self,*args,**kwargs):
        super(DiscussionPost, self).save(*args,**kwargs)
        channel_layer = get_channel_layer()
        notification_count=DiscussionPost.objects.all()
        data = serializers.serialize('json', list(notification_count), fields=('title','time','name','user'))
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',{
                'type':'send_notification',
                'value':data
            }
        )

    def __str__(self):
        return self.title
    
    class Meta:
         ordering = ['-time']


class CommentForm(models.Model):
    discussion = models.ForeignKey(
        DiscussionPost, on_delete=CASCADE, null=True, related_name='comments')
    comment = models.CharField(max_length=200)
    name = models.CharField(max_length=80, null=True)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.comment


class Like(models.Model):
    discussion = models.ForeignKey(
        DiscussionPost, on_delete=CASCADE, null=True, related_name='likes')
    fromUser = models.ForeignKey(
        User, on_delete=CASCADE, null=True, related_name='fromUser')
    toUser = models.ForeignKey(
        User, on_delete=CASCADE, null=True, related_name='toUser')
    name = models.CharField(max_length=80, null=True)
    message = models.CharField(max_length=200)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.name
