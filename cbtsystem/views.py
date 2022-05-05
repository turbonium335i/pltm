from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *

# fix origin django 4.0 csrf error

def index(request):

    firstTest = testSpec.objects.all().first()

    return render(request, 'cbtsystem/index.html', {"firstTest" : firstTest} )

def demo(request):

    return render(request, 'cbtsystem/demo.html' )

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

    return render(request, 'cbtsystem/loginpage.html' )


def logoutpage(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect('loginpage')

def breakPage(request):

    return render(request, 'cbtsystem/break.html' )

def directions(request):

    return render(request, 'cbtsystem/directions.html' )

def results(request):

    return render(request, 'cbtsystem/results.html' )




@csrf_exempt
def endsection(request):

    data = json.loads(request.body)
    print(data['ls'])
    print(data['timeLeft'])
    print(data['section'])
    print(data['user_id'])

    progressRecord, created= testInProgress.objects.get_or_create(studentId="1")

    print(progressRecord)

    rAnswers = json.loads(data['ls'])
    rTimeLeft = json.loads(data['timeLeft'])
    progressRecord.studentAnswersReading = rAnswers
    progressRecord.timeLeftReading = rTimeLeft
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


def processtest(request):

    testData = testInProgress.objects.all().first()
    testQuery = testSpec.objects.all().first()

    # print(testQuery.questionType)
    # for x, y in testQuery.questionType.items():
    #     print(x, y)
    # testQuery = (testData[0].studentAnswersReading)

    return render(request, 'cbtsystem/processTest.html', {"testData": testData, "testQuery": testQuery})

