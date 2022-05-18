from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
import collections
from django.contrib.auth.decorators import login_required

from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


# fix origin django 4.0 csrf error


@login_required(login_url='loginpage')
def index(request):

    username = request.user
    record = testRecord.objects.filter(studentUsername=username.username).order_by('-id')


    inProgress = testInProgress.objects.filter(studentId=username.id).first()

    testQ = groupTest.objects.all()
    # query manytomany relationship
    testGroup = testQ[0].showTest.all()

    percentR = 0
    percentW = 0


    try:
        inProgressTest = int(inProgress.testId)
        testQuery = testSpec.objects.get(id=inProgress.testId)
        percentR = (round((len(inProgress.studentAnswersReading)/len(testQuery.answerKeyReading))*100))
        percentW = (round((len(inProgress.studentAnswersWriting) / len(testQuery.answerKeyWriting)) * 100))

    except:
        inProgressTest = ""

    print("inProgressTest", inProgressTest)

    # if inProgressTest != "":


    return render(request, 'cbtsystem/index.html', {"inProgress": inProgress,
                                                    "testGroup": testGroup,
                                                    "record": record,
                                                    "inProgressTest": inProgressTest,
                                                    "percentR": percentR,
                                                    "percentW": percentW,
                                                    })

@login_required(login_url='loginpage')
def demo(request):
    return render(request, 'cbtsystem/demo.html')


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userx = authenticate(request, username=username, password=password)

        if userx is not None:
            login(request, userx)
            current_user = request.user
            if current_user == request.user.is_superuser:
                return redirect('index')

            else:
                try:
                    return redirect('index')
                except:
                    return redirect('index')
        else:
            messages.info(request, "USERNAME and/or PASSWORD is incorrect.")

    return render(request, 'cbtsystem/loginpage.html')


def logoutpage(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect('loginpage')

@login_required(login_url='loginpage')
def breakPage(request):
    return render(request, 'cbtsystem/break.html')

@login_required(login_url='loginpage')
def directions(request):
    return render(request, 'cbtsystem/directions.html')

@login_required(login_url='loginpage')
def directions2(request):
    return render(request, 'cbtsystem/directions2.html')

@login_required(login_url='loginpage')
def results(request):
    qNo = []
    qMarked = []
    qAnswer = []
    qType = []

    record = testRecord.objects.all().first()
    testQuery = testSpec.objects.all().first()

    for n, a in record.studentAnswersReading.items():
        qNo.append(n)
        qMarked.append(a)

    for n, a in testQuery.answerKeyReading.items():
        qAnswer.append(a)

    for n, a in testQuery.questionTypeReading.items():
        qType.append(a)

    zipRecord = zip(qNo, qMarked, qAnswer, qType)

    qNo = []
    qMarked = []
    qAnswer = []
    qType = []

    for n, a in record.studentAnswersWriting.items():
        qNo.append(n)
        qMarked.append(a)

    for n, a in testQuery.answerKeyWriting.items():
        qAnswer.append(a)

    for n, a in testQuery.questionTypeWriting.items():
        qType.append(a)

    zipRecordW = zip(qNo, qMarked, qAnswer, qType)

    return render(request, 'cbtsystem/results.html',
                  {"zipRecord": zipRecord, "zipRecordW": zipRecordW, "record": record})

@login_required(login_url='loginpage')
def results_pk(request, pk):
    qNo = []
    qMarked = []
    qAnswer = []
    qType = []

    try:

        record = testRecord.objects.get(id=pk)

        if request.user.username == record.studentUsername:

            testQuery = testSpec.objects.all().first()

            for n, a in record.studentAnswersReading.items():
                qNo.append(n)
                qMarked.append(a)

            for n, a in testQuery.answerKeyReading.items():
                qAnswer.append(a)

            for n, a in testQuery.questionTypeReading.items():
                qType.append(a)

            zipRecord = zip(qNo, qMarked, qAnswer, qType)

            qNo = []
            qMarked = []
            qAnswer = []
            qType = []

            for n, a in record.studentAnswersWriting.items():
                qNo.append(n)
                qMarked.append(a)

            for n, a in testQuery.answerKeyWriting.items():
                qAnswer.append(a)

            for n, a in testQuery.questionTypeWriting.items():
                qType.append(a)

            zipRecordW = zip(qNo, qMarked, qAnswer, qType)

            return render(request, 'cbtsystem/results.html',
                          {"zipRecord": zipRecord, "zipRecordW": zipRecordW, "record": record})
        else:
            return redirect("index")

    except:

        logout(request)
        messages.info(request, "Authentication Error")
        return redirect('loginpage')

@login_required(login_url='loginpage')
def cbtwriting(request):
    return render(request, 'cbtsystem/cbtwriting.html')


@login_required(login_url='loginpage')
def history(request):
    username = request.user.username
    record = testRecord.objects.filter(studentUsername=username)
    return render(request, 'cbtsystem/history.html', {'record': record})


@csrf_exempt
def endsection(request):
    try:
        data = json.loads(request.body)
        print(data['ls'], data['timeLeft'], data['section'], data['section'], data['user_id'], data['selectedTestId'],  data['selectedTest'])


        progressRecord, created = testInProgress.objects.get_or_create(studentId=request.user.id)

        print(progressRecord)

        rAnswers = json.loads(data['ls'])

        if data['section'] == 'reading':

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersReading = rAnswers
            progressRecord.timeLeftReading = rTimeLeft

        else:

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersWriting = rAnswers
            progressRecord.timeLeftWriting = rTimeLeft

        progressRecord.studentUsername = request.user.username
        progressRecord.studentName = request.user.first_name
        progressRecord.studentId = request.user.id
        progressRecord.testName = data['selectedTest']
        progressRecord.testId = data['selectedTestId']
        progressRecord.save(force_insert=False)


        # save progress every 5 questions?

        # multiqsetName, created = groupmulti.objects.get_or_create(multiqsetName=makegroupsetname)
        # multiqsetName.multiq.add(toadd)
        # multiqsetName.save(force_insert=False)

        return JsonResponse('progress saved', safe=False)

    except:
        return JsonResponse('data incomplete', safe=False)

@login_required(login_url='loginpage')
def processtest(request):

    username = request.user

    try:
        testData = testInProgress.objects.get(studentId=username.id)
        testQuery = testSpec.objects.get(id=testData.testId)

        inCorrect = []
        wrongQtype = []

        studentAnswersR = testData.studentAnswersReading
        studentAnswersW = testData.studentAnswersWriting
        readingAnswerKey = testQuery.answerKeyReading
        writingAnswerKey = testQuery.answerKeyWriting

        cleanAnswerR = {}
        cleanAnswerW = {}

        for k, v in readingAnswerKey.items():
            try:
                cleanAnswerR[k] = studentAnswersR[k]
            except:
                cleanAnswerR[k] = 'X'

        for k, v in writingAnswerKey.items():
            try:
                cleanAnswerW[k] = studentAnswersW[k]
            except:
                cleanAnswerW[k] = 'X'

        studentAnswersR = cleanAnswerR
        studentAnswersW = cleanAnswerW

        # return JsonResponse( cleanAnswerW, safe=False)

        print(testData.statusReading, testData.statusWriting)

        for x, y in studentAnswersR.items():
            if y != readingAnswerKey[x]:
                inCorrect.append(x)
                wrongQtype.append(testQuery.questionTypeReading[x])

        wrongQ = dict(collections.Counter(wrongQtype))
        wrongSortR = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
        numberInCorrectR = str(len(inCorrect))
        print("Reading: -" + str(len(inCorrect)) + ",", wrongSortR)

        inCorrect = []
        wrongQtype = []

        for x, y in studentAnswersW.items():
            # print(x, y, testQuery.answerKeyReading[x])
            if y != writingAnswerKey[x]:
                inCorrect.append(x)
                wrongQtype.append(testQuery.questionTypeWriting[x])

        wrongQ = dict(collections.Counter(wrongQtype))
        wrongSortW = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
        numberInCorrectW = str(len(inCorrect))
        print("Writing: -" + str(len(inCorrect)) + ",", wrongSortW)

        r = testRecord.objects.create(studentUsername=username.username,
                                      studentName=username.first_name,
                                      testName=testData.testName,
                                      testId=testData.testId,
                                      studentAnswersReading=studentAnswersR,
                                      studentAnswersWriting=studentAnswersW,
                                      numberInCorrectR=numberInCorrectR,
                                      numberInCorrectW=numberInCorrectW,
                                      jsonWrongQtypeR=wrongSortR,
                                      jsonWrongQtypeW=wrongSortW
                                      )

        print('record saved: ', r)

        testData.delete()

        # return render(request, 'cbtsystem/processTest.html', {"testData": testData, "testQuery": testQuery})
        return render(request, 'cbtsystem/processTestClaw.html')

    except:

        return render(request, 'cbtsystem/processTestClaw.html' )

        # logout(request)
        # messages.info(request, "Authentication Error")
        # return redirect('loginpage')


@login_required(login_url='loginpage')
@api_view(['GET'])
def pendingTestApi(request):
    pendingTests = testInProgress.objects.all()
    serializer = progressSerializer(pendingTests, many=True)
    return Response(serializer.data)

