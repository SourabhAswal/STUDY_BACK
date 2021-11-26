from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from .serializers import SaveQuestionSerializer
from .models import QuizQuestion
from django.http import QueryDict


@api_view(['POST'])
def savequestion(request):
    print(request.data)
    serializer = SaveQuestionSerializer(data=request.data)
    # id = request.data['subsecid']
    # print(id)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Question added successfully',
        }
        return Response(response, status=status_code)
    return Response({"error": "Please provide details"})


# @api_view(['POST'])
# def submitquestion(request):
#     print(request.data)
#     question=request.data['questions']
#     print(question)
#     print(type(question))
#     option = request.data['options']
#     options = option.split(',')
#     print(type(options))
#     for i in range(len(options)):
#         print(options[i])
#     for i in options(4):
#         options[i]=

#     serializer = SaveQuestionsSerializer(data=question)
#     if serializer.is_valid():
#         serializer.save()
#         status_code = status.HTTP_200_OK
    #     response = {
    #         'success': 'True',
    #         'status code': status_code,
    #         'message': 'Question added successfully',
    #     }
    #     return Response(response, status=status_code)
    # return Response({"error": "Please provide details"})

@api_view(['POST'])
def submitquestion(request):
    print(request.data)
    question = request.data['questions']
    ques = question.split(',')
    option = request.data['options']
    opt = option.split(',')
    answers = request.data['answer']
    ans = answers.split(',')
    coursesubsecid = request.data['coursesubsec_id']
    print(coursesubsecid)
    print(ques)
    print(opt)
    print(ans)
    for i in range(len(ques)):
        j = i*4

        p = QuizQuestion(question=ques[i], option1=opt[j], option2=opt[j+1],
                         option3=opt[j+2], option4=opt[j+3], answer=ans[i], coursesubsec_id_id=coursesubsecid)
        p.save()
    serializer = SaveQuestionSerializer()

    status_code = status.HTTP_200_OK
    response = {
        'success': 'True',
        'status code': status_code,
        'message': 'Question added successfully',
    }
    return Response(response, status=status_code)
