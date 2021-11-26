import json
from django.db.models import F
from django.http.response import Http404
from rest_framework import status, viewsets
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from userauthn.serializers import User
from .seralizers import AllCourseSerializer, CourseSerializer, MemberSerializer, uploadPdfSerializer, UploadPptSerializer, UploadSubVideoSerializer,subSectionIdSerializer
from .models import Course, Member, CourseSec, UploadPpt, Uploadpdf, UploadSubVideo,lastSubsectionVisited
from rest_framework.response import Response
from .seralizers import CourseSerializer, MemberSerializer, CourseSecSerializer, CourseSubSecSerializer
from .models import Course, Member, CourseSec, CourseSubSec
from rest_framework.permissions import IsAuthenticated
from google.cloud import storage
from .seralizers import CourseSerializer, MemberSerializer, CourseAllDataSerializer
from .models import Course, Member
from django.http import HttpResponse
from django.conf import settings
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView
from .exceptions import FileNotUploaded
from django.db import IntegrityError
from course import seralizers
import urllib.request

# create,read,update and delete course


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def create(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid:
            img = request.data.get('course_img')
            video = request.data.get('course_video')
            client = storage.Client()
            bucket = client.get_bucket(
                settings.GOOGLE_CLOUD_STORAGE_BUCKET)
            object_name_in_gcs_bucket = bucket.blob(img.name)
            object_name_in_gcs_bucket.upload_from_string(img.file.read())
            video_url = upload_content_blob(
                settings.GOOGLE_CLOUD_STORAGE_BUCKET, video, "videocontent/"+video.name)
            Course.objects.create(course_img=settings.GOOGLE_CLOUD_STORAGE_URL+img.name, course_name=request.data['course_name'], organization=request.data['organization'], course_start_datetime=request.data['course_start_datetime'], course_end_datetime=request.data['course_end_datetime'], course_des=request.data['course_des'],
                                  course_video=settings.GOOGLE_CLOUD_STORAGE_URL+"videocontent/"+video.name,
                                  course_prerequisite=request.data['course_prerequisite'])
            return Response({'status': 'success', 'status_code': status.HTTP_201_CREATED})
        return Response({'status': 'error', 'status_code': status.HTTP_400_BAD_REQUEST})
    # except Exception as e:
    #     return Response({'status':'exception'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        course = Course.objects.get(id=pk)
        serializer = CourseSerializer(instance=course, data=request.data)
        img = request.FILES.get('course_img')
        video = request.FILES.get('course_video')
        try:
            if img and video:
                client = storage.Client()
                bucket = client.get_bucket(
                    settings.GOOGLE_CLOUD_STORAGE_BUCKET)
                object_name_in_gcs_bucket = bucket.blob(img.name)
                object_name_in_gcs_bucket.upload_from_string(img.file.read())
                video_url = upload_content_blob(
                    settings.GOOGLE_CLOUD_STORAGE_BUCKET, video, "videocontent/"+video.name)
                Course.objects.filter(id=pk).update(course_name=request.data['course_name'], organization=request.data['organization'], course_start_datetime=request.data['course_start_datetime'], course_end_datetime=request.data['course_end_datetime'],
                                                    course_img=settings.GOOGLE_CLOUD_STORAGE_URL+img.name, course_des=request.data['course_des'],
                                                    course_video=settings.GOOGLE_CLOUD_STORAGE_URL+"videocontent/"+video.name,
                                                    course_prerequisite=request.data['course_prerequisite'])
                return Response({'status': 'success', 'status_code': status.HTTP_201_CREATED})
            elif img:
                client = storage.Client()
                bucket = client.get_bucket(
                    settings.GOOGLE_CLOUD_STORAGE_BUCKET)
                object_name_in_gcs_bucket = bucket.blob(img.name)
                object_name_in_gcs_bucket.upload_from_string(img.file.read())
                Course.objects.filter(id=pk).update(course_name=request.data['course_name'], organization=request.data['organization'], course_start_datetime=request.data['course_start_datetime'], course_end_datetime=request.data['course_end_datetime'],
                                                    course_img=settings.GOOGLE_CLOUD_STORAGE_URL+img.name, course_des=request.data['course_des'],
                                                    course_prerequisite=request.data['course_prerequisite'])
                return Response({'status': 'success', 'status_code': status.HTTP_201_CREATED})
            elif video:
                video_url = upload_content_blob(
                    settings.GOOGLE_CLOUD_STORAGE_BUCKET, video, "videocontent/"+video.name)

                Course.objects.filter(id=pk).update(course_name=request.data['course_name'], organization=request.data['organization'], course_start_datetime=request.data['course_start_datetime'], course_end_datetime=request.data['course_end_datetime'],
                                                    course_video=settings.GOOGLE_CLOUD_STORAGE_URL+"videocontent/"+video.name, course_des=request.data['course_des'],
                                                    course_prerequisite=request.data['course_prerequisite'])
                return Response({'status': 'success', 'status_code': status.HTTP_201_CREATED})

            else:
                Course.objects.filter(id=pk).update(course_name=request.data['course_name'], organization=request.data['organization'], course_start_datetime=request.data['course_start_datetime'], course_end_datetime=request.data['course_end_datetime'],
                                                    course_des=request.data['course_des'],

                                                    course_prerequisite=request.data['course_prerequisite'])
                return Response({'status': 'success', 'status_code': status.HTTP_200_OK})
        except IntegrityError as e:
            return Response({'status': 'fail'})

    def list(self, request):
        queryset = Course.objects.all()
        sorted_queryset= queryset.order_by('-id')
        print(queryset.order_by('-id'))
        serializer = AllCourseSerializer(sorted_queryset, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    # def destroy(self,request, pk):
    #     courseSec = Course.objects.get(id=pk)
    #     courseSec.delete()
    #     return Response({'status':'true','status_code':status.HTTP_200_OK})
    #     # return Response('Item succsesfully delete!')

    def destroy(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
            course_img_url = course.course_img.split("/")
            blob_name = course_img_url[4]
            delete_blob(settings.GOOGLE_CLOUD_STORAGE_BUCKET, blob_name)
            course.delete()
            return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
        except course.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})

    def get_queryset(self):
        course = Course.objects.all().order_by('id')
        # print(course)
        return course


def destroy_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer

    def get_queryset(self):
        member = Member.objects.all().order_by('id')
        return member

    def create(self, request, *args, **kwargs):
        course = Course.objects.get(id=request.data['c_Id'])
        user = User.objects.get(id=request.data['user'])
        query = Member.objects.filter(c_Id=course, user=user)

        if(len(query) == 0):
            Member.objects.create(c_Id=course, user=user)
            return Response({'status': 'true', 'status_code': '200', 'message': 'course enrolled successfully'})
        else:
            return Response({'status': 'error', 'status_code': '400', 'message': 'Already enrolled'})


class Check_courseVisited(APIView):
    def put(self, request, userId, courseId):
        try:
            if courseId != None and userId != None:
                Member.objects.filter(c_Id=courseId, user=userId).update(
                    has_visited='True')
                return Response({"status": "success", "status_code": "200"})
            else:
                return Response("invalid course or user Id")
        except Member.DoesNotExist:
            raise Http404


# Enroll course api
@api_view(['GET', 'POST', ])
def enroll_course(request):
    userId = request.data.get('userId')
    pubs = Member.objects.select_related('c_Id').filter(user=userId).values(
        'has_visited', 'c_Id', course_name=F("c_Id__course_name"), course_img=F("c_Id__course_img"))
    data = list(pubs.values())
    return Response(data)


# Unenroll course api
@api_view(['POST'])
def unenroll(request):
    course_id = request.data['course_id']
    user_id = request.data['userId']
    if Member.objects.filter(c_Id=course_id, user=user_id):
        Member.objects.filter(c_Id=course_id, user=user_id)[0].delete()
    return HttpResponse("UnEnrolled Successfull")


# get Course section on the basis of course id
@api_view(['GET'])
def courseSecList(request, pk):
    coursesSec = CourseSec.objects.filter(course=pk)
    serializer = CourseSecSerializer(coursesSec, many=True)
    return Response(serializer.data)


# create course section
@api_view(['POST'])
def courseSecCreate(request):
    serializer = CourseSecSerializer(data=request.data)
    id = request.data['id']
    course = Course.objects.get(id=id)
    try:
     if serializer.is_valid():
        section = CourseSec(course=course, title=serializer.data['title'])
        section.save()
        return Response({'status': 'true'}) 
     else:
        return Response({'status': 'fail'})   

    except Exception as e:
        return Response({'status': 'fail'})

# update course section


@api_view(['POST'])
def courseSecUpdate(request, pk):
    courseSec = CourseSec.objects.get(id=pk)
    serializer = CourseSecSerializer(instance=courseSec, data=request.data)
    try:
     if serializer.is_valid():
        serializer.save()
        return Response({'status': 'true'}) 
     else:
        return Response({'status': 'fail'})  
    except Exception as e:
        return Response({'status': 'fail'})


# delete course section
@api_view(['POST'])
def courseSecDelete(request, pk):
    courseSec = CourseSec.objects.get(id=pk)
    courseSec.delete()

    return Response('Item succsesfully delete!')


# get all course sections
class CourseSecList(ListCreateAPIView):
    queryset = CourseSec.objects.all()
    serializer_class = CourseSecSerializer
    # permission_classes = [IsAuthenticated,]

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = CourseSecSerializer(queryset, many=True)
            return Response({'status': 'true', 'sections': serializer.data, 'staus_code': status.HTTP_200_OK})
        except Exception as e:
            return Response({'status': 'exception', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


# Get Course Sub Section on the basis of section id
@api_view(['GET'])
def courseSubSecList(request, pk):
    courseSubSec = CourseSubSec.objects.filter(courseSub=pk)
    serializer = CourseSubSecSerializer(courseSubSec, many=True)
    return Response(serializer.data)


# create course subsection api
@api_view(['POST'])
def courseSubSecCreate(request):
    serializer = CourseSubSecSerializer(data=request.data)
    id = request.data['id']
    course = CourseSec.objects.get(id=id)
    try:
      if serializer.is_valid():
        section = CourseSubSec(courseSub=course, sub=serializer.data['sub'])
        section.save()
        return Response({'status': 'true'}) 
      else:
        return Response({'status': 'fail'})   

    except Exception as e:
        
         return Response({'status': 'fail'})   

# get all subsections api


class CourseSubSecList(ListCreateAPIView):
    queryset = CourseSubSec.objects.all()
    serializer_class = CourseSubSecSerializer
    # permission_classes = [IsAuthenticated,]

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = CourseSubSecSerializer(queryset, many=True)
            return Response({'status': 'true', 'subsections': serializer.data, 'staus_code': status.HTTP_200_OK})
        except Exception as e:
            return Response({'status': 'exception', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


@api_view(['POST'])
def courseSubSecUpdate(request, pk):
    courseSec = CourseSubSec.objects.get(id=pk)
    serializer = CourseSubSecSerializer(instance=courseSec, data=request.data)
    try:
     if serializer.is_valid():
        serializer.save()
        return Response({'status': 'true'}) 
     else:
        return Response({'status': 'fail'})     
    except Exception as e:
        return Response({'status': 'fail'})


@api_view(['POST'])
def courseSubSecDelete(request, pk):
    courseSec = CourseSubSec.objects.get(id=pk)
    courseSec.delete()

    return Response('Item succsesfully delete!')


# upload pdf and presentation api
class UploadPdf(GenericAPIView):
    # permission_class= (IsAuthenticated,)
    queryset = Uploadpdf.objects.all()
    serializer_class = uploadPdfSerializer

    def post(self, request):
        try:
            pdf_serializer = self.serializer_class(data=request.data)
            id = request.data['id']
            coursesubsection = CourseSubSec.objects.get(id=id)
            exists = Uploadpdf.objects.filter(
                display_name=request.data['display_name'])
            if exists:
                return Response({'status': 'false', 'detail': 'PDF already uploaded', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
            else:
                if 'pdf' in request.FILES or pdf_serializer.is_valid:
                    pdf = request.FILES.getlist('pdf')
                    for file in pdf:
                        try:
                            public_url = upload_blob(
                                settings.GOOGLE_CLOUD_STORAGE_BUCKET, file, "pdfcontent/"+file.name)
                        except Exception as err:
                            # logger.error("Unable to upload file {} due to {}".format(file, str(err)))
                            raise Exception("Write to gcp failed!")
                        course_pdf = Uploadpdf(
                            display_name=request.data['display_name'], pdf=public_url, courseSubSection=coursesubsection)
                        course_pdf.save()

                return Response({'status': 'true'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'exception', 'detail': 'Internal server error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})

    def delete(self, request, pk):
        try:
            pdfObj = Uploadpdf.objects.get(id=pk)
            pdf_url = pdfObj.pdf.split("/")
            blob_name = pdf_url[5]
            delete_blob(settings.GOOGLE_CLOUD_STORAGE_BUCKET,
                        "pdfcontent/"+blob_name)
            pdfObj.delete()
            return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
        except pdfObj.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})

    def put(self, request, pk):
        try:
            pdfObj = Uploadpdf.objects.get(id=pk)
            id = request.data['id']
            coursesubsection = CourseSubSec.objects.get(id=id)
            pdf = request.FILES.get('pdf')
            if pdf:
                if request.data['display_name'] != "":
                    public_url = upload_blob(
                        settings.GOOGLE_CLOUD_STORAGE_BUCKET, pdf, "pdfcontent/"+pdf.name)
                    Uploadpdf.objects.filter(id=pk).update(
                        display_name=request.data['display_name'], pdf=public_url, courseSubSection=coursesubsection)
                    return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
                else:
                    return Response({
                        'status': 'true',
                        'status_code': status.HTTP_200_OK
                    })
            else:
                if request.data['display_name'] != "":
                    Uploadpdf.objects.filter(id=pk).update(
                        display_name=request.data['display_name'], courseSubSection=coursesubsection)
                    return Response({
                        'status': 'true',
                        'status_code': status.HTTP_200_OK
                    })
                else:
                    return Response({
                        'status': 'false',
                        'message': 'Provide valid display name'
                    })
        except pdfObj.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})

    def get(self, request, pk):
        pdf_list = Uploadpdf.objects.filter(id=pk)
        serializer = uploadPdfSerializer(pdf_list, many=True)
        print(serializer)
        return Response(serializer.data)


class ViewUploadPdfAPI(GenericAPIView):
    serializer_class = uploadPdfSerializer

    def get(self, request, pk):
        try:
            pdf = Uploadpdf.objects.filter(courseSubSection=pk)
            if(pdf.exists() == False):
                raise FileNotUploaded("PDF not available for this subsection")
            else:
                pdf_uploaded = Uploadpdf.objects.filter(courseSubSection=pk)
                serializer = self.serializer_class(pdf_uploaded, many=True)
                return Response(
                    {'success': 'true',
                     'data': serializer.data
                     })
        except FileNotUploaded as e:
            return Response({
                'success': 'false',
                'message': e.message
            })
        except Exception as e:
            return Response({
                'success': 'false',
                'message': 'Some problem occurred.'
            })


def upload_content_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source_file_name.file.read())


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.content_type = "application/pdf"
    if source_file_name.content_type == "application/pdf":
        blob.upload_from_string(
            source_file_name.file.read(), content_type='application/pdf')
        return(blob.public_url)
    else:
        blob.upload_from_string(source_file_name.file.read())

# method to delete object on GCP


def delete_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    stats = storage.Blob(bucket=bucket, name=blob_name).exists(storage_client)
    blob = bucket.blob(blob_name)
    if stats:
        blob.delete()


class UploadPptAPIView(GenericAPIView):
    serializer_class = UploadPptSerializer
    queryset = UploadPpt.objects.all()

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            id = request.data['id']
            courseSubSection = CourseSubSec.objects.get(id=id)
            exists = UploadPpt.objects.filter(
                display_name=request.data['displayName'])
            if exists:
                return Response({'status': 'false', 'detail': 'PPT already uploaded', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
            if 'ppt' in request.FILES and serializer.is_valid:
                ppt = request.FILES.getlist('ppt')
                for file in ppt:
                    upload_content_blob(
                        settings.GOOGLE_CLOUD_STORAGE_BUCKET, file, "pptcontent/"+file.name)
                    course_ppt = UploadPpt(
                        display_name=request.data['displayName'], ppt=settings.GOOGLE_CLOUD_STORAGE_URL+"pptcontent/"+file.name, courseSubSection=courseSubSection)
                    course_ppt.save()

            return Response({'status': 'true'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'exception', 'detail': 'Internal server error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})

    def delete(self, request, pk):

        try:
            pptobj = UploadPpt.objects.get(id=pk)
            pdf_url = pptobj.ppt.split("/")
            blob_name = pdf_url[5]
            delete_blob(settings.GOOGLE_CLOUD_STORAGE_BUCKET,
                        "pptcontent/"+blob_name)
            pptobj.delete()
            return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
        except pptobj.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})

    def get(self, request, pk):

        try:
            ppt = UploadPpt.objects.filter(courseSubSection=pk)
            if ppt.exists() == False:
                raise FileNotUploaded('No PPT available for this subsection')
            else:
                uploaded_ppt = UploadPpt.objects.filter(courseSubSection=pk)
                serializer = self.serializer_class(uploaded_ppt, many=True)
                return Response({
                    'success': 'true',
                    'data': serializer.data
                })
        except FileNotUploaded as e:
            return Response({
                'success': 'false',
                'message': e.message
            })
        except Exception as e:
            return Response({
                'success': 'false',
                'message': 'Some problem occurred.'
            })

    # def put(self, request, pk):
    #     try:
    #         ppt = Uploadpdf.objects.get(id=pk)
    #         id = request.data['id']
    #         coursesubsection = CourseSubSec.objects.get(id=id)
    #         pptFiles = request.FILES.get('ppt')
    #         if pptFiles:
    #             public_url = upload_blob(
    #                 settings.GOOGLE_CLOUD_STORAGE_BUCKET, pptFiles, "pptcontent/"+pptFiles.name)
    #         else:
    #             raise ValidationError({'status': 'please upload pdf first'})
    #         UploadPpt.objects.filter(id=pk).update(
    #             display_name=request.data['displayName'], ppt=public_url, courseSubSection=coursesubsection)
    #         return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
    #     except ppt.DoesNotExist:
    #         return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})
    # def put(self, request, pk):
    #     try:
    #         ppt = UploadPpt.objects.get(id=pk)
    #         id = request.data['id']
    #         coursesubsection = CourseSubSec.objects.get(id=id)
    #         if 'ppt' in request.FILES:
    #             ppt = request.FILES.getlist('ppt')
    #             for file in ppt:
    #                 upload_content_blob(
    #                     settings.GOOGLE_CLOUD_STORAGE_BUCKET, file, "pptcontent/"+file.name)
    #         UploadPpt.objects.filter(id=pk).update(
    #             display_name=request.data['displayName'], ppt=settings.GOOGLE_CLOUD_STORAGE_URL+"pptcontent/"+file.name, courseSubSection=coursesubsection)
    #         # subSectionVideo.save()
    #         return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
        # except ppt.DoesNotExist:
        #     return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})

    def put(self, request, pk):
        try:
            pptObj = UploadPpt.objects.get(id=pk)
            id = request.data['id']
            coursesubsection = CourseSubSec.objects.get(id=id)
            ppt = request.FILES.get('ppt')
            if ppt:
                if request.data['displayName'] != "":
                    public_url = upload_content_blob(
                        settings.GOOGLE_CLOUD_STORAGE_BUCKET, ppt, "pptcontent/"+ppt.name)
                    UploadPpt.objects.filter(id=pk).update(
                        display_name=request.data['displayName'], ppt=public_url, courseSubSection=coursesubsection)
                    return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
            else:
                if request.data['displayName'] != "":
                    UploadPpt.objects.filter(id=pk).update(
                        display_name=request.data["displayName"], courseSubSection=coursesubsection)
                    return Response({
                        'status': 'true',
                        'status_code': status.HTTP_200_OK
                    })
        except pptObj.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})


class GetPptAPIView(GenericAPIView):
    def get(self, request, pk):
        ppt_List = UploadPpt.objects.filter(id=pk)
        serializer = UploadPptSerializer(ppt_List, many=True)
        return Response(serializer.data)


class CourseAllDataAPIView(ListAPIView):
    serializer_class = CourseAllDataSerializer
    queryset = Course.objects.all()

    def get(self, request, pk):
        self.queryset = Course.objects.get(id=pk)
        serializer = self.serializer_class(self.queryset, many=False)
        return Response(serializer.data)


class UploadSubVideoAPIView(GenericAPIView):
    serializer_class = UploadSubVideoSerializer
    queryset = UploadSubVideo.objects.all()

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            id = request.data['id']
            courseSubSection = CourseSubSec.objects.get(id=id)
            exists = UploadSubVideo.objects.filter(
                subvideoName=request.data['subvideoName'], courseSubSection=courseSubSection)
            if exists:
                return Response({'status': 'false', 'detail': 'Video already uploaded', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
            if 'subVideo' in request.FILES or serializer.is_valid:
                subVideo = request.FILES.getlist('subVideo')
                for file in subVideo:
                    upload_content_blob(
                        settings.GOOGLE_CLOUD_STORAGE_BUCKET, file, "subVideocontent/"+file.name)
                    subSectionVideo = UploadSubVideo(
                        subvideoName=request.data['subvideoName'], subVideo=settings.GOOGLE_CLOUD_STORAGE_URL+"subVideocontent/"+file.name, external=False, courseSubSection=courseSubSection)
                    subSectionVideo.save()

            return Response({'status': 'true'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'exception', 'detail': 'Internal server error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})

    def get(self, request, pk):
        try:
            subSecVideo = UploadSubVideo.objects.filter(
                courseSubSection=pk)
            if subSecVideo.exists() == False:
                raise FileNotUploaded("No video uploaded for this subsection")
            else:
                subSecVideo = UploadSubVideo.objects.filter(
                    courseSubSection=pk)
                serializer = self.serializer_class(subSecVideo, many=True)
                # print(subSecVideo)
                return Response({
                    'success': 'true',
                    'data': serializer.data
                })

        except FileNotUploaded as e:
            return Response({
                'success': 'false',
                'message': e.message
            })
        except Exception as e:
            return Response({
                'success': 'false',
                'message': 'Some problem occurred.'
            })

    def delete(self, request, pk):

        try:
            pdfObj = UploadSubVideo.objects.get(id=pk)
            pdf_url = pdfObj.subVideo.split("/")
            blob_name = pdf_url[5]
            delete_blob(settings.GOOGLE_CLOUD_STORAGE_BUCKET,
                        "subVideocontent/"+blob_name)
            pdfObj.delete()
            return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
        except pdfObj.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})

    def put(self, request, pk):
        try:
            print(request.data)
            video = UploadSubVideo.objects.get(id=pk)
            id = request.data['id']
            coursesubsection = CourseSubSec.objects.get(id=id)
            subvideo = request.FILES.get('subVideo')
            if subvideo:
                if request.data['subvideoName'] != "":
                    public_url = upload_content_blob(
                        settings.GOOGLE_CLOUD_STORAGE_BUCKET, subvideo.name, "subVideocontent/"+subvideo.name)
                    print(public_url)
                    UploadSubVideo.objects.filter(id=pk).update(
                        subvideoName=request.data['subvideoName'], subVideo=public_url, courseSubSection=coursesubsection, external=False)
                    return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
            else:
                if request.data['subvideoName'] != "":
                    UploadSubVideo.objects.filter(id=pk).update(
                        subvideoName=request.data['subvideoName'], courseSubSection=coursesubsection)
                    return Response({
                        'status': 'true',
                        'status_code': status.HTTP_200_OK
                    })
        except video.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})


class UploadExternalVideoAPIView(GenericAPIView):
    serializer_class = UploadSubVideoSerializer
    queryset = UploadSubVideo.objects.all()

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            id = request.data['id']
            courseSubSection = CourseSubSec.objects.get(id=id)
            exists = UploadSubVideo.objects.filter(
                subVideo=request.data['extVideoLink'], courseSubSection=courseSubSection)
            if exists:
                return Response({
                    'status': 'false',
                    'message': 'Video Url already present'
                })

            if serializer.is_valid:
                extVideo = UploadSubVideo(
                    subvideoName=request.data['extVideoName'], subVideo=request.data['extVideoLink'], courseSubSection=courseSubSection, external=True)
                extVideo.save()
                return Response({
                    'status': 'true',
                    'message': 'External Video Uploaded Successfully',
                })
        except Exception as e:
            return Response({
                'status': 'exception',
                'message': 'Some Error Occurred',
            })

    def delete(self, request, pk):
        try:
            extVideo = UploadSubVideo.objects.get(id=pk)
            extVideo.delete()
            return Response({
                'status': 'true',
            })
        except Exception as e:
            return Response({
                'status': 'exception'
            })

    def put(self, request, pk):
        try:
            extVideo = UploadSubVideo.objects.filter(id=pk)
            serializer = self.serializer_class(
                instance=extVideo, data=request.data, many=False)
            if serializer.is_valid:
                UploadSubVideo.objects.filter(id=pk).update(
                    subvideoName=request.data['subvideoName'], subVideo=request.data['subVideo'], external=True)
                return Response({
                    'status': 'true',
                    'message': 'External Video Updated successfully'
                })
            return Response({
                'status': 'false',
                'message': 'External Video not updated'
            })
        except Exception as e:
            return Response({
                'status': 'exception',
                'message': 'Some Error occured'
            })

    def get(self, request, pk):
        extVideo = UploadSubVideo.objects.get(id=pk)
        serializer = UploadSubVideoSerializer(extVideo, many=False)
        return Response(serializer.data)


class getSubVideoAPIView(GenericAPIView):
    def get(self, request, pk):
        subVideo_List = UploadSubVideo.objects.filter(id=pk)
        serializer = UploadSubVideoSerializer(subVideo_List, many=True)
        return Response(serializer.data)

class defaultsubIDAPIView(GenericAPIView):
    serializer_class = subSectionIdSerializer
    queryset = lastSubsectionVisited.objects.all()
    

    def post(self, request):
       
        
        try:
            print(request.data)
            id = request.data['id']
            if(lastSubsectionVisited.objects.filter(course_Id=id).exists()):
                course = Course.objects.get(id=id)
                lastSubsectionVisited.objects.filter(course_Id=id).update(course_Id=course,subsection_id=request.data['subsection_id'])
                return Response({'status': 'true'}, status=status.HTTP_201_CREATED)
            else:
                print("hello")
                course = Course.objects.get(id=id)
                course_sub_id = lastSubsectionVisited(course_Id=course,subsection_id=request.data['subsection_id'])
                course_sub_id.save()
                return Response({'status': 'true'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'exception', 'detail': 'Internal server error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
    def get(self, request,pk):
        # try:
         defaultList = lastSubsectionVisited.objects.filter(course_Id=pk)
         serializer = subSectionIdSerializer(defaultList, many=True)
         return Response(serializer.data)
        # except Exception as e:
        #     return Response({'status': 'exception', 'detail': 'Internal server error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}) 

    def delete(self, request, pk):

        try:
            defaultsubobj = lastSubsectionVisited.objects.get(course_Id=pk)
           
            defaultsubobj.delete()
            return Response({'status': 'true', 'status_code': status.HTTP_200_OK})
        except defaultsubobj.DoesNotExist:
            return Response({'status': 'exception', 'status_code': status.HTTP_204_NO_CONTENT})
# class GetDefaultsubIdAPIView(GenericAPIView):
#     serializer_class = subSectionIdSerializer
#     queryset = lastSubsectionVisited.objects.all()
#     def get(self, request, pk):
#         defaultList = lastSubsectionVisited.objects.filter(id=pk)
#         serializer = subSectionIdSerializer(defaultList, many=True)
#         return Response(serializer.data)