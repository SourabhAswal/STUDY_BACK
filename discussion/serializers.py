from django.db.models import fields
from course import models, seralizers
from rest_framework import serializers
from .models import DiscussionPost, CommentForm, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentForm
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = DiscussionPost
        fields = ['id', 'user', 'name', 'title', 'body', 'time', 'comments', 'likes']
        depth = 1


class DiscussionPostSerializer(seralizers.MemberSerializer):
    class Meta:
        model = DiscussionPost
        fields ='__all__'