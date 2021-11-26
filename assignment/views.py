from django.shortcuts import render
from rest_framework import generics
from .serializers import AssignmentSerializer, AssignmentFileSerializer
from .models import Assignment, AssignmentFile
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage
from django.conf import settings
import json
from userauthn.models import CustomUser
from course.models import CourseSubSec, CourseSec, Course
from userauthn.serializers import AllUsersSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from course.exceptions import FileNotUploaded


class AssignmentAPI(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response({
                'success': 'True',
                'message': 'Success',
                'status code': status.HTTP_200_OK
            })
        return Response({'fail': 'Please fill all the required fields!'})

    def get(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response({
            'success': 'True',
            'data': serializer.data
        })


class AssignmentEditAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get(self, request, pk):
        try:
            obj = Assignment.objects.filter(subsectionid=pk)
            if obj.exists() == False:
                raise FileNotUploaded("No Assignment available for this subsection")
            else:
                self.queryset = Assignment.objects.filter(subsectionid=pk)
                serializer = self.serializer_class(self.queryset, many=True)
                return Response({
                    'status': 'True',
                    'data': serializer.data
                })
        except FileNotUploaded as e:
            return Response({
                'status': 'False',
                'message': e.message
            })
        except Exception as e:
            return Response({
                'status': 'False',
                'message': "Some problem occurred"
            })

    def delete(self, request, pk):
        self.queryset = Assignment.objects.filter(id=pk).delete()
        serializer = self.serializer_class(self.queryset, many=False)
        return Response({
            'success': 'True',
            'message': "Delete successfull"
        })


class AssignmentFileAPI(generics.ListCreateAPIView):
    queryset = AssignmentFile.objects.all()
    serializer_class = AssignmentFileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer = self.serializer_class(self.queryset, many=True)
        if serializer.is_valid:
            subsecname = request.data.get('subsecName')
            secname = request.data.get('secName')
            coursename = request.data.get('courseName')
            userid = request.data.get('userid')
            susecid = request.data.get('subsecid')
            first_name = request.data.get('first_name')
            assignment = request.data.get('assignmentfile')
            assignment_url = upload_Assignment_blob(settings.GOOGLE_CLOUD_STORAGE_BUCKET, assignment, "assignmentcontent/"+assignment.name)
            AssignmentFile.objects.create(
                assignmentFile=settings.GOOGLE_CLOUD_STORAGE_URL+"assignmentcontent/"+assignment.name, userid=request.data['userid'],
                subsecid_id=request.data['subsecid'], first_name=request.data['first_name'], courseName=request.data['courseName'],
                secName=request.data['secName'],subsecName=request.data['subsecName'])
            return Response({
                'success': 'True',
                'message': 'Successfully Submitted',
                'status code': status.HTTP_200_OK
            })
        return Response({'fail': 'Please try again!'})


class UsersDataAPI(generics.GenericAPIView):
    serializer_class = AssignmentFileSerializer
    def get(self, request):
        self.queryset = AssignmentFile.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response({
            'status': 'True',
            'data': serializer.data,
        })

# def upload_Assignment_blob(bucket_name, source_file_name, destination_blob_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_string(source_file_name.file.read())

def upload_Assignment_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source_file_name.file.read())
    return blob.public_url