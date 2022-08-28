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

    try:
        testGroup = testQ[0].showTest.all()

    except:
        testGroup = []

    percentR = 0
    percentW = 0

    try:
        inProgressTest = int(inProgress.testId)
        testQuery = testSpec.objects.get(id=inProgress.testId)
        percentR = (round((len(inProgress.studentAnswersReading) / len(testQuery.answerKeyReading)) * 100))
        percentW = (round((len(inProgress.studentAnswersWriting) / len(testQuery.answerKeyWriting)) * 100))

    except:
        inProgressTest = ""


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


@login_required(login_url='loginpage')
def cbtreading(request, pk):
    testQ = groupTest.objects.all()[0]

    try:

        testPDF = testQ.showTest.get(id=pk)

        return render(request, 'cbtsystem/cbtreading.html', {'testPDF': testPDF})

    except:
        logout(request)
        messages.info(request, "Authentication Error")
        return redirect('loginpage')


@login_required(login_url='loginpage')
def cbtwriting(request, pk):

    testQ = groupTest.objects.all()[0]

    try:

        testPDF = testQ.showTest.get(id=pk)

        return render(request, 'cbtsystem/cbtwriting.html', {'testPDF': testPDF})

    except:
        logout(request)
        messages.info(request, "Authentication Error")
        return redirect('loginpage')

@login_required(login_url='loginpage')
def cbtmathone(request, pk):

    testQ = groupTest.objects.all()[0]

    try:

        testPDF = testQ.showTest.get(id=pk)

        return render(request, 'cbtsystem/cbtmathone.html', {'testPDF': testPDF})

    except:
        logout(request)
        messages.info(request, "Authentication Error")
        return redirect('loginpage')

@login_required(login_url='loginpage')
def cbtmathtwo(request, pk):

    testQ = groupTest.objects.all()[0]

    try:

        testPDF = testQ.showTest.get(id=pk)

        return render(request, 'cbtsystem/cbtmathtwo.html', {'testPDF': testPDF})

    except:
        logout(request)
        messages.info(request, "Authentication Error")
        return redirect('loginpage')



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
def directionsm1(request):
    return render(request, 'cbtsystem/directionsm1.html')

@login_required(login_url='loginpage')
def directionsm2(request):
    return render(request, 'cbtsystem/directionsm2.html')


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

        testqnotes = QtypeNote.objects.all()
        testnotesdict = {}

        for x in testqnotes:
            testnotesdict[x.title] = x.notes

        record = testRecord.objects.get(id=pk)

        if request.user.username == record.studentUsername:

            testQuery = testSpec.objects.get(id=record.testId)

            for n, a in record.studentAnswersReading.items():
                qNo.append(n)
                qMarked.append(a)

            for n, a in testQuery.answerKeyReading.items():
                qAnswer.append(a)

            for n, a in testQuery.questionTypeReading.items():
                qType.append(a)

            ziptypesQnotesR = []

            for zz in qType:
                try:
                    ziptypesQnotesR.append(testnotesdict[zz])
                except:
                    ziptypesQnotesR.append("Question Type input error. Contact administrator.")

            zipRecord = zip(qNo, qMarked, qAnswer, qType, ziptypesQnotesR)

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

            ziptypesQnotesW = []

            for zz in qType:
                try:
                    ziptypesQnotesW.append(testnotesdict[zz])
                except:
                    ziptypesQnotesW.append("Question Type input error. Contact administrator.")

            zipRecordW = zip(qNo, qMarked, qAnswer, qType, ziptypesQnotesW)

            return render(request, 'cbtsystem/results.html',
                          {"zipRecord": zipRecord, "zipRecordW": zipRecordW, "record": record})
        else:
            return redirect("index")

    except:

        # logout(request)
        # messages.info(request, "Authentication Error")
        return redirect('index')





@login_required(login_url='loginpage')
def history(request):
    username = request.user.username
    record = testRecord.objects.filter(studentUsername=username)
    return render(request, 'cbtsystem/history.html', {'record': record})


@csrf_exempt
def endsection(request):
    try:
        data = json.loads(request.body)
        print(data['ls'], data['timeLeft'], data['section'],
              data['section'], data['user_id'], data['selectedTestId'],
              data['selectedTest'], data['testStatus'])

        progressRecord, created = testInProgress.objects.get_or_create(studentId=request.user.id)

        print(progressRecord)

        rAnswers = json.loads(data['ls'])

        if data['section'] == 'reading':

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersReading = rAnswers
            progressRecord.timeLeftReading = rTimeLeft

        elif data['section'] == 'math1':

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersMathOne = rAnswers
            progressRecord.timeLeftMathOne = rTimeLeft

        elif data['section'] == 'math2':

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersMathTwo = rAnswers
            progressRecord.timeLeftMathTwo = rTimeLeft

        else:

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersWriting = rAnswers
            progressRecord.timeLeftWriting = rTimeLeft

        progressRecord.studentUsername = request.user.username
        progressRecord.studentName = request.user.first_name
        progressRecord.studentId = request.user.id
        progressRecord.testName = data['selectedTest']
        progressRecord.testId = data['selectedTestId']

        if data['testStatus'] == 'r':
            progressRecord.statusReading = "YES"

        if data['testStatus'] == 'w':
            progressRecord.statusWriting = "YES"

        if data['testStatus'] == 'm1':
            progressRecord.statusMathOne = "YES"

        if data['testStatus'] == 'm2':
            progressRecord.statusMathTwo = "YES"


        progressRecord.save(force_insert=False)


        return JsonResponse('progress saved', safe=False)

    except:
        return JsonResponse('data incomplete', safe=False)


@login_required(login_url='loginpage')
def processtest(request):
    username = request.user

    # try:
    testData = testInProgress.objects.get(studentId=username.id)
    testQuery = testSpec.objects.get(id=testData.testId)

    print('test status: ', testData.statusReading, testData.statusWriting,
          testData.studentAnswersReading, testData.studentAnswersWriting

          )

    if (testData.statusReading == 'YES' and testData.statusWriting == 'YES'):
        correct = []
        inCorrect = []

        correctQtype = []
        wrongQtype = []

        studentAnswersR = testData.studentAnswersReading
        studentAnswersW = testData.studentAnswersWriting
        readingAnswerKey = testQuery.answerKeyReading
        writingAnswerKey = testQuery.answerKeyWriting

        readingQT = testQuery.questionTypeReading
        writingQT = testQuery.questionTypeWriting


        qTypeTotalR = []

        for k, v in readingQT.items():
            qTypeTotalR.append(v)

        qTypeTotalR= dict(collections.Counter(qTypeTotalR))


        qTypeTotalW = []

        for k, v in writingQT.items():
            qTypeTotalW.append(v)

        qTypeTotalW= dict(collections.Counter(qTypeTotalW))


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

        for x, y in studentAnswersR.items():
            if y != readingAnswerKey[x]:
                inCorrect.append(x)
                wrongQtype.append(testQuery.questionTypeReading[x])
            else:
                correct.append(x)
                correctQtype.append(testQuery.questionTypeReading[x])

        wrongQ = dict(collections.Counter(wrongQtype))
        wrongSortR = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
        numberInCorrectR = str(len(inCorrect))
        print("Reading: -" + numberInCorrectR + ",", wrongSortR)

        # correctQ = dict(collections.Counter(correctQtype))
        # correctSortR = dict(sorted(correctQ.items(), key=lambda item: item[1], reverse=True))
        # numberCorrectR = str(len(correct))
        # print("Reading: +" + numberCorrectR + ",", correctSortR)


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
        print("Writing: -" + numberInCorrectW + ",", wrongSortW)

        qTypePercentR = {}

        for x, y in qTypeTotalR.items():

            try:
                qTypePercentR[x] = round(100 * ((int(qTypeTotalR[x]) - int(wrongSortR[x]))/int(qTypeTotalR[x])))
            except:
                qTypePercentR[x] = 100

        jsonQtypePerR = dict(sorted(qTypePercentR.items(), key=lambda item: item[1], reverse=True))
        print('R % correct: ', jsonQtypePerR)

        qTypePercentW = {}

        for x, y in qTypeTotalW.items():

            try:
                qTypePercentW[x] = round(100 * ((int(qTypeTotalW[x]) - int(wrongSortW[x]))/int(qTypeTotalW[x])))
            except:
                qTypePercentW[x] = 100


        jsonQtypePerW = dict(sorted(qTypePercentW.items(), key=lambda item: item[1], reverse=True))
        print('W % correct: ', jsonQtypePerW)



        r = testRecord.objects.create(studentUsername=username.username,
                                      studentName=username.first_name,
                                      testName=testData.testName,
                                      testId=testData.testId,
                                      studentAnswersReading=studentAnswersR,
                                      studentAnswersWriting=studentAnswersW,
                                      numberInCorrectR=numberInCorrectR,
                                      numberInCorrectW=numberInCorrectW,
                                      jsonWrongQtypeR=wrongSortR,
                                      jsonWrongQtypeW=wrongSortW,
                                      jsonQtypePerR=jsonQtypePerR,
                                      jsonQtypePerW=jsonQtypePerW
                                      )

        print('record saved: ', r)

        testData.delete()

        # return render(request, 'cbtsystem/processTest.html', {"testData": testData, "testQuery": testQuery})
        return render(request, 'cbtsystem/processTestClaw.html')
    else:
        return redirect('index')


    # except:
    #
    #     # return render(request, 'cbtsystem/processTestClaw.html')
    #     return redirect('index')

        # logout(request)
        # messages.info(request, "Authentication Error")
        # return redirect('loginpage')


@login_required(login_url='loginpage')
@api_view(['GET'])
def pendingTestApi(request):
    pendingTests = testInProgress.objects.all()
    serializer = progressSerializer(pendingTests, many=True)
    return Response(serializer.data)


@login_required(login_url='loginpage')
def rawscale(request):
    raw = []
    reading = []
    writing = []
    score = []
    ptest = {58: ['None0', 'None0', 800], 57: ['None0', 'None0', 790], 56: ['None0', 'None0', 780],
             55: ['None0', 'None0', 770], 54: ['None0', 'None0', 750], 53: ['None0', 'None0', 740],
             52: ['400', 'None0', 730], 51: ['390', 'None0', 710], 50: ['380', 'None0', 710], 49: ['370', 'None0', 700],
             48: ['370', 'None0', 690], 47: ['360', 'None0', 680], 46: ['360', 'None0', 670], 45: ['350', 'None0', 660],
             44: ['340', '400', 660], 43: ['330', '390', 640], 42: ['330', '380', 640], 41: ['320', '370', 630],
             40: ['320', '360', 620], 39: ['310', '350', 610], 38: ['310', '340', 600], 37: ['300', '330', 600],
             36: ['300', '330', 590], 35: ['290', '320', 580], 34: ['290', '320', 570], 33: ['280', '310', 560],
             32: ['280', '300', 550], 31: ['270', '290', 540], 30: ['270', '290', 540], 29: ['260', '280', 530],
             28: ['260', '280', 520], 27: ['250', '270', 520], 26: ['250', '260', 510], 25: ['240', '260', 500],
             24: ['240', '250', 490], 23: ['230', '250', 480], 22: ['230', '240', 470], 21: ['220', '230', 460],
             20: ['220', '220', 450], 19: ['210', '220', 440], 18: ['210', '210', 430], 17: ['200', '210', 420],
             16: ['190', '200', 410], 15: ['190', '190', 400], 14: ['180', '190', 380], 13: ['180', '180', 370],
             12: ['170', '170', 360], 11: ['170', '170', 350], 10: ['160', '160', 330], 9: ['150', '150', 320],
             8: ['150', '140', 310], 7: ['140', '140', 290], 6: ['130', '130', 280], 5: ['120', '120', 260],
             4: ['110', '110', 250], 3: ['100', '100', 230], 2: ['100', '100', 210], 1: ['100', '100', 200],
             0: ['100', '100', 200]}
    topper = {800: ['99+', 99], 790: ['99+', 99], 780: ['99+', 98], 770: ['99', 97], 760: ['99', 96], 750: ['98', 96],
              740: ['98', 95], 730: ['97', 94], 720: ['96', 93], 710: ['95', 92], 700: ['94', 91], 690: ['93', 90],
              680: ['91', 89], 670: ['90', 87], 660: ['88', 86], 650: ['86', 84], 640: ['83', 82], 630: ['81', 81],
              620: ['78', 79], 610: ['76', 77], 600: ['73', 75], 590: ['70', 72], 580: ['67', 69], 570: ['64', 66],
              560: ['60', 64], 550: ['57', 61], 540: ['54', 58], 530: ['50', 54], 520: ['47', 50], 510: ['44', 46],
              500: ['40', 42], 490: ['37', 39], 480: ['34', 36], 470: ['30', 33], 460: ['27', 30], 450: ['24', 27],
              440: ['21', 24], 430: ['18', 22], 420: ['15', 19], 410: ['13', 17], 400: ['11', 15], 390: ['9', 12],
              380: ['7', 10], 370: ['5', 8], 360: ['4', 7], 350: ['3', 5], 340: ['2', 4], 330: ['1', 3], 320: ['1', 2],
              310: ['1', 1], 300: ['1', 1], 290: ['1', 1], 280: ['1', 1], 270: ['1', 1], 260: ['1', 1], 250: ['1', 1],
              240: ['1', 1], 230: ['1', 1], 220: ['1', 1], 210: ['1', 1], 200: ['1', 1]}
    topscore = []
    topverbal = []
    topmath = []

    for k, v in ptest.items():
        raw.append(k)
        reading.append(v[0])
        writing.append(v[1])
        score.append(v[2])
    moo = zip(raw, reading, writing, score)

    for k, v in topper.items():
        topscore.append(k)
        topverbal.append(v[0])
        topmath.append(v[1])

    foo = zip(topscore, topverbal, topmath)

    return render(request, 'cbtsystem/rawscale.html', {'moo': moo, 'foo': foo})
