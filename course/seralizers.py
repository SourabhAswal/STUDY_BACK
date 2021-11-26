from rest_framework import serializers
from .models import Course, Member, CourseSec, CourseSubSec, UploadPpt, Uploadpdf,UploadSubVideo,lastSubsectionVisited
from assignment.serializers import AssignmentSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'organization', 'course_start_datetime', 'course_end_datetime',
                  'course_des', 'course_img', 'course_video', 'course_prerequisite']

class AllCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'c_Id', 'user']

class uploadPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uploadpdf
        fields = '__all__'


class UploadPptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadPpt
        fields = '__all__'
class UploadSubVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadSubVideo
        fields = '__all__'



class CourseSubSecSerializer(serializers.ModelSerializer):
    pdf = uploadPdfSerializer(read_only=True, many=True)
    ppt = UploadPptSerializer(read_only=True, many=True)
    assignment = AssignmentSerializer(read_only=True, many=True)
    subVideo = UploadSubVideoSerializer(read_only=True, many=True)
    class Meta:
        model = CourseSubSec
        fields = ['id', 'sub', 'courseSub_id', 'pdf', 'ppt', 'assignment', 'subVideo']


class CourseSecSerializer(serializers.ModelSerializer):
    subSection = CourseSubSecSerializer(read_only=True, many=True)
    class Meta:
        model = CourseSec
        fields = ['id', 'title', 'course_id', 'subSection']


class CourseAllDataSerializer(serializers.ModelSerializer):
    sections = CourseSecSerializer(read_only=True, many=True)


    class Meta:
        model = Course
        fields = ['id', 'course_name', 'organization', 'course_start_datetime', 'course_end_datetime',
                  'course_des', 'course_img', 'course_video', 'course_prerequisite', 'sections']

class subSectionIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = lastSubsectionVisited
        fields = '__all__'

