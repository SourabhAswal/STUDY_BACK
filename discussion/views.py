from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import DiscussionPostSerializer, DiscussionSerializer, CommentSerializer, LikeSerializer

from .models import CommentForm, DiscussionPost, Like
from course.models import Course
from Super_Admin.models import Role
from userauthn.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView

import datetime
import pytz

User = get_user_model()

class DiscussionAllData(ListAPIView):
    serializer_class = DiscussionSerializer
    queryset = DiscussionPost.objects.all()

    def get(self, request, pk):
        self.queryset = DiscussionPost.objects.filter(
            course=pk).order_by('-id')
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

class CreatePost(ListCreateAPIView):
    queryset = DiscussionPost.objects.all()
    serializer_class = DiscussionPostSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Post created successfully',
            }
            return Response(response, status=status_code)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }

        return Response(response, status=status_code)


class UpdatePost(UpdateAPIView):

    queryset = DiscussionPost.objects.all()
    serializer_class = DiscussionPostSerializer

    def update(self, request, pk, *args, **kwargs):
        post = DiscussionPost.objects.get(id=pk)
        serializer = self.serializer_class(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Post updated successfully',
            }
            return Response(response, status=status_code)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }

        return Response(response, status=status_code)

@api_view(['DELETE'])
def discussionDelete(request, pk):
    try:
        discussion = DiscussionPost.objects.get(id=pk)
        discussion.delete()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Comment deleted successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }

    return Response(response, status=status_code)


@api_view(['GET'])
def commentList(request):
    comment = CommentForm.objects.all().order_by('-id')
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)

class CreateComment(ListCreateAPIView):
    queryset = CommentForm.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Comment created successfully',
            }
            return Response(response, status=status_code)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }

        return Response(response, status=status_code)


class UpdateComment(UpdateAPIView):

    queryset = CommentForm.objects.all()
    serializer_class = CommentSerializer

    def update(self, request, pk, *args, **kwargs):
        comment = CommentForm.objects.get(id=pk)
        serializer = self.serializer_class(instance=comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Post updated successfully',
            }
            return Response(response, status=status_code)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }

        return Response(response, status=status_code)


@api_view(['DELETE'])
def commentDelete(request, pk):
    try:
        comment = CommentForm.objects.get(id=pk)
        comment.delete()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Comment deleted successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }

    return Response(response, status=status_code)


@api_view(['GET'])
def likeList(request):
    like = Like.objects.all().order_by('id')
    serializer = LikeSerializer(like, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def likeEdit(request):
    try:
        discussion = DiscussionPost.objects.get(id=request.data['postId'])
        user = User.objects.get(id=request.data['userId'])
        check = Like.objects.filter(
            discussion=discussion, toUser=user, name=request.data['name'])
        if(check):
            check.delete()
        else:
            like = Like(discussion=discussion, toUser=user,
                        name=request.data['name'])
            like.save()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Updated successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Something went wrong',
        }
        
    return Response(response, status=status_code)
