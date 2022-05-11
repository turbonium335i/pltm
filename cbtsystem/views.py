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


# fix origin django 4.0 csrf error


# @login_required(login_url='loginpage')
def index(request):
    firstTest = testSpec.objects.all().first()
    inProgress = testInProgress.objects.all().last()
    testQ = groupTest.objects.all()
    # query manytomany relationship
    testGroup = testQ[0].showTest.all()

    return render(request, 'cbtsystem/index.html', {"firstTest": firstTest,
                                                    "inProgress": inProgress,
                                                    "testGroup": testGroup,
                                                    })


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


def breakPage(request):
    return render(request, 'cbtsystem/break.html')


def directions(request):
    return render(request, 'cbtsystem/directions.html')


def directions2(request):
    return render(request, 'cbtsystem/directions2.html')


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

        return redirect("index")


def cbtwriting(request):
    return render(request, 'cbtsystem/cbtwriting.html')


# @login_required(login_url='index')
def history(request):
    username = request.user.username
    record = testRecord.objects.filter(studentUsername=username)
    return render(request, 'cbtsystem/history.html', {'record': record})


@csrf_exempt
def endsection(request):
    try:
        data = json.loads(request.body)
        print(data['ls'])
        print(data['timeLeft'])
        print(data['section'])
        print(data['user_id'])

        progressRecord, created = testInProgress.objects.get_or_create(studentId="2")

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

        progressRecord.save(force_insert=False)

        #                                           (studentUsername="bobUsername",
        #                                           studentName="bobName",
        #                                           testName="bobTest",
        #                                           studentAnswersReading=data,
        #                                           studentAnswersWriting=data,
        #                                           )

        # save progress every 5 questions?

        # multiqsetName, created = groupmulti.objects.get_or_create(multiqsetName=makegroupsetname)
        # multiqsetName.multiq.add(toadd)
        # multiqsetName.save(force_insert=False)

        return JsonResponse('progress saved', safe=False)

    except:
        return JsonResponse('data incomplete', safe=False)


def processtest(request):
    testData = testInProgress.objects.all().first()
    testQuery = testSpec.objects.all().first()

    inCorrect = []
    wrongQtype = []

    studentAnswersR = testData.studentAnswersReading
    studentAnswersW = testData.studentAnswersWriting

    print(testData.statusReading, testData.statusWriting)

    for x, y in testData.studentAnswersReading.items():
        # print(x, y, testQuery.answerKeyReading[x])
        if y != testQuery.answerKeyReading[x]:
            inCorrect.append(x)
            wrongQtype.append(testQuery.questionTypeReading[x])

    wrongQ = dict(collections.Counter(wrongQtype))
    wrongSortR = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
    numberInCorrectR = str(len(inCorrect))
    print("Reading: -" + str(len(inCorrect)) + ",", wrongSortR)

    inCorrect = []
    wrongQtype = []

    for x, y in testData.studentAnswersWriting.items():
        # print(x, y, testQuery.answerKeyReading[x])
        if y != testQuery.answerKeyWriting[x]:
            inCorrect.append(x)
            wrongQtype.append(testQuery.questionTypeWriting[x])

    wrongQ = dict(collections.Counter(wrongQtype))
    wrongSortW = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
    numberInCorrectW = str(len(inCorrect))
    print("Writing: -" + str(len(inCorrect)) + ",", wrongSortW)

    # r = testRecord.objects.create(studentUsername='bobcatUser',
    #                               studentName='bobcat kim',
    #                               testName='bobcat testName',
    #                               studentAnswersReading=studentAnswersR,
    #                               studentAnswersWriting=studentAnswersW,
    #                               numberInCorrectR=numberInCorrectR,
    #                               numberInCorrectW=numberInCorrectW,
    #                               jsonWrongQtypeR=wrongSortR,
    #                               jsonWrongQtypeW=wrongSortW
    #                               )

    print(testRecord.objects.all().last())

    return render(request, 'cbtsystem/processTest.html', {"testData": testData, "testQuery": testQuery})
