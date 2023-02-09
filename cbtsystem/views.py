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
from django.contrib.admin.views.decorators import staff_member_required

from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import *

from datetime import datetime, timedelta


# fix origin django 4.0 csrf error


@login_required(login_url='loginpage')
def index(request):
    username = request.user
    record = testRecord.objects.filter(studentUsername=username.username).order_by('-id')

    inProgress = testInProgress.objects.filter(studentId=username.id).first()

    testQ = groupTest.objects.all()
    # query manytomany relationship

    uName = User.objects.get(username=username).id
    allowedTest = accountprofile.objects.get(userAccount=uName).allowed.all()
    print(allowedTest)
    # testQ = accountprofile.objects.all()

    try:
        testGroup = testQ[0].showTest.all()

    except:
        testGroup = []

    percentR = 0
    percentW = 0
    percentMA1 = 0
    percentMA2 = 0

    try:
        inProgressTest = int(inProgress.testId)
    except:
        inProgressTest = ""

    try:
        testQuery = testSpec.objects.get(id=inProgress.testId)
        percentR = (round((len(inProgress.studentAnswersReading) / len(testQuery.answerKeyReading)) * 100))
        percentW = (round((len(inProgress.studentAnswersWriting) / len(testQuery.answerKeyWriting)) * 100))
        percentMA1 = (round((len(inProgress.studentAnswersMathOne) / len(testQuery.answerKeyMathOne)) * 100))
        percentMA2 = (round((len(inProgress.studentAnswersMathTwo) / len(testQuery.answerKeyMathTwo)) * 100))

    except:
        pass

    nextTest = testDate.objects.all().first()
    # print(nextTest.next_test.strftime("new Date(%Y, %m, %d)"))

    return render(request, 'cbtsystem/index.html', {"inProgress": inProgress,
                                                    "testGroup": testGroup,
                                                    "record": record,
                                                    "inProgressTest": inProgressTest,
                                                    "percentR": percentR,
                                                    "percentW": percentW,
                                                    "percentMA1": percentMA1,
                                                    "percentMA2": percentMA2,
                                                    "nextTest": nextTest,
                                                    'allowedTest': allowedTest,
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

        try:
            testPDF = accountprofile.objects.get(request.user.id).allowed.all()[0]

            return render(request, 'cbtsystem/cbtreading.html', {'testPDF': testPDF})
        except:
            # logout(request)
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
            uName = User.objects.get(username=username).id
            try:
                status = accountprofile.objects.get(userAccount=uName).status
            except:
                messages.info(request, "No Account Profile")
                return redirect('loginpage')

            if status == True:
                login(request, userx)
                current_user = request.user
                return redirect('index')
            else:
                messages.info(request, "Account not active.")
                return redirect('loginpage')
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

    qNo = []
    qMarked = []
    qAnswer = []
    qType = []

    for n, a in record.studentAnswersMathOne.items():
        qNo.append(n)
        qMarked.append(a)
    for n, a in testQuery.answerKeyMathOne.items():
        qAnswer.append(a)
    for n, a in testQuery.questionTypeMathOne.items():
        qType.append(a)

    zipRecordM1 = zip(qNo, qMarked, qAnswer, qType)

    qNo = []
    qMarked = []
    qAnswer = []
    qType = []

    for n, a in record.studentAnswersMathTwo.items():
        qNo.append(n)
        qMarked.append(a)
    for n, a in testQuery.answerKeyMathTwo.items():
        qAnswer.append(a)
    for n, a in testQuery.questionTypeMathTwo.items():
        qType.append(a)

    zipRecordM2 = zip(qNo, qMarked, qAnswer, qType)

    return render(request, 'cbtsystem/results.html',
                  {"zipRecord": zipRecord, "zipRecordW": zipRecordW,
                   "record": record,
                   "zipRecordM1": zipRecordM1,
                   "zipRecordM2": zipRecordM2,
                   })


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

        if request.user.username == record.studentUsername or request.user.is_superuser:

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

            qNo = []
            qMarked = []
            qAnswer = []
            qType = []

            for n, a in record.studentAnswersMathOne.items():
                qNo.append(n)
                qMarked.append(a)

            for n, a in testQuery.answerKeyMathOne.items():
                qAnswer.append(a)

            for n, a in testQuery.questionTypeMathOne.items():
                qType.append(a)

            ziptypesQnotesM1 = []

            for zz in qType:
                try:
                    ziptypesQnotesM1.append(testnotesdict[zz])
                except:
                    ziptypesQnotesM1.append("Question Type input error. Contact administrator.")

            zipRecordM1 = zip(qNo, qMarked, qAnswer, qType, ziptypesQnotesM1)

            qNo = []
            qMarked = []
            qAnswer = []
            qType = []

            for n, a in record.studentAnswersMathTwo.items():
                qNo.append(n)
                qMarked.append(a)

            for n, a in testQuery.answerKeyMathTwo.items():
                qAnswer.append(a)

            for n, a in testQuery.questionTypeMathTwo.items():
                qType.append(a)

            ziptypesQnotesM2 = []

            for zz in qType:
                try:
                    ziptypesQnotesM2.append(testnotesdict[zz])
                except:
                    ziptypesQnotesM2.append("Question Type input error. Contact administrator.")

            zipRecordM2 = zip(qNo, qMarked, qAnswer, qType, ziptypesQnotesM2)

            return render(request, 'cbtsystem/results.html',
                          {"zipRecord": zipRecord, "zipRecordW": zipRecordW,
                           "zipRecordM1": zipRecordM1, "zipRecordM2": zipRecordM2,
                           "record": record})
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


@login_required(login_url='loginpage')
def update(request):
    record = testRecord.objects.all().order_by('-id')

    # rawVerbal = verbalKeyLen - (int(numberInCorrectR) + int(numberInCorrectW))
    # rawMath = mathKeyLen - (int(numberInCorrectM1) + int(numberInCorrectM2))
    #
    # readingscore = newraw[rawVerbal][0]
    # mathscore = newraw[rawMath][1]

    for i in record:
        testQuery = testSpec.objects.get(id=i.testId)
        verbalKeyLen = len(testQuery.answerKeyReading) + len(testQuery.answerKeyWriting)
        mathKeyLen = len(testQuery.answerKeyMathOne) + len(testQuery.answerKeyMathTwo)

        rawVerbal = (int(i.numberInCorrectR) + int(i.numberInCorrectW))
        rawMath = (int(i.numberInCorrectM1) + int(i.numberInCorrectM2))

        print(i.scoreReading, i.scoreMath, rawVerbal, rawMath)

        if i.scoreReading == "200":

            try:
                readingscore = newraw[rawVerbal][0]
                mathscore = newraw[rawMath][1]

                i.scoreReading = newraw[rawVerbal][0]
                i.scoreMath = newraw[rawMath][1]
                i.save()
                print(readingscore, mathscore)
            except:
                pass

    return render(request, 'cbtsystem/update.html', {'record': record})


@staff_member_required(login_url='loginpage')
def staff(request):
    username = request.user.username
    record = testRecord.objects.all().order_by('-id')

    queryList = []
    qs = '1, 2, 3, 4, 5'
    v1 = {}
    v2 = {}
    m1 = {}
    m2 = {}
    q_test = ''

    if request.method == 'POST':
        qs = request.POST.get("queryids")
        try:
            qs = [int(x.strip()) for x in qs.split(',')]
            for q in qs:
                try:
                    queryList.append(testRecord.objects.get(id=q))
                except:
                    messages.warning(request, f"ID:{q} invalid!")
        except:
            messages.warning(request, "Form Error")

        statsv1 = {}
        statsv2 = {}
        statsm1 = {}
        statsm2 = {}

        if len(queryList) > 0:
            try:
                q_test = testSpec.objects.get(id=queryList[0].testId)
            except:
                messages.warning(request, "Queried Test Invaild")

            for n in range(1, (len(queryList[0].studentAnswersReading) + 1)):
                statsv1[str(n)] = []
            for q in queryList:
                x = q.studentAnswersReading
                for k, v in x.items():
                    statsv1[str(k)].append(v)

            for n in range(1, (len(queryList[0].studentAnswersWriting) + 1)):
                statsv2[str(n)] = []
            for q in queryList:
                x = q.studentAnswersWriting
                for k, v in x.items():
                    statsv2[str(k)].append(v)

            for n in range(1, (len(queryList[0].studentAnswersMathOne) + 1)):
                statsm1[str(n)] = []
            for q in queryList:
                x = q.studentAnswersMathOne
                for k, v in x.items():
                    statsm1[str(k)].append(v)

            for n in range(1, (len(queryList[0].studentAnswersMathTwo) + 1)):
                statsm2[str(n)] = []
            for q in queryList:
                x = q.studentAnswersMathTwo
                for k, v in x.items():
                    statsm2[str(k)].append(v)

        try:
            qDict = q_test.answerKeyReading
            for k, v in statsv1.items():
                v1[k] = [dict(collections.Counter(v)), qDict[k]]
                # v1[k] = dict(collections.Counter(v))
            qDict = q_test.answerKeyWriting
            for k, v in statsv2.items():
                v2[k] = [dict(collections.Counter(v)), qDict[k]]

            qDict = q_test.answerKeyMathOne
            for k, v in statsm1.items():
                m1[k] = [dict(collections.Counter(v)), qDict[k]]

            qDict = q_test.answerKeyMathTwo
            for k, v in statsm2.items():
                m2[k] = [dict(collections.Counter(v)), qDict[k]]
        except:
            return render(request, 'cbtsystem/staff.html', {'record': record,
                                                            'queryList': queryList,
                                                            'v1': v1,
                                                            'v2': v2,
                                                            'm1': m1,
                                                            'm2': m2,
                                                            'q_test': q_test,
                                                            'qs': qs})

    return render(request, 'cbtsystem/staff.html', {'record': record,
                                                    'queryList': queryList,
                                                    'v1': v1,
                                                    'v2': v2,
                                                    'm1': m1,
                                                    'm2': m2,
                                                    'q_test': q_test,
                                                    'qs': qs})


@csrf_exempt
def endsection(request):
    data = json.loads(request.body)
    print(data['ls'], data['timeLeft'], data['section'],
          data['section'], data['user_id'], data['selectedTestId'],
          data['selectedTest'], data['testStatus'])

    try:
        data = json.loads(request.body)
        print(data['ls'], data['timeLeft'], data['section'],
              data['section'], data['user_id'], data['selectedTestId'],
              data['selectedTest'], data['testStatus'])

        progressRecord, created = testInProgress.objects.get_or_create(studentId=request.user.id)

        rAnswers = json.loads(data['ls'])

        if data['section'] == 'reading':

            rTimeLeft = json.loads(data['timeLeft'])
            progressRecord.studentAnswersReading = rAnswers
            progressRecord.timeLeftReading = rTimeLeft

            if data['selectedTestId'] != progressRecord.testId:
                progressRecord.studentAnswersMathOne = {}
                progressRecord.studentAnswersWriting = {}
                progressRecord.studentAnswersMathTwo = {}

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
        progressRecord.date_started = datetime.now()
        progressRecord.save()

        return JsonResponse('progress saved', safe=False)

    except:
        return JsonResponse('data incomplete', safe=False)


newraw = {66: [200, 200], 65: [200, 200], 64: [200, 200], 63: [200, 200], 62: [200, 200], 61: [200, 200],
          60: [200, 200],
          59: [200, 200], 58: [200, 200], 57: [200, 200], 56: [200, 200], 55: [200, 200], 54: [200, 200],
          53: [210, 200],
          52: [220, 200], 51: [230, 200], 50: [240, 200], 49: [250, 200], 48: [260, 200], 47: [270, 200],
          46: [280, 200],
          45: [290, 200], 44: [300, 200], 43: [310, 220], 42: [330, 230], 41: [340, 240], 40: [350, 250],
          39: [360, 280],
          38: [380, 300], 37: [390, 320], 36: [400, 340], 35: [410, 350], 34: [430, 360], 33: [440, 380],
          32: [460, 390],
          31: [470, 400], 30: [490, 410], 29: [500, 430], 28: [510, 440], 27: [520, 450], 26: [530, 460],
          25: [540, 480],
          24: [550, 490], 23: [560, 500], 22: [570, 510], 21: [580, 520], 20: [590, 530], 19: [600, 540],
          18: [610, 550],
          17: [620, 560], 16: [630, 570], 15: [640, 580], 14: [650, 590], 13: [660, 600], 12: [670, 610],
          11: [680, 620],
          10: [690, 630], 9: [700, 650], 8: [710, 660], 7: [720, 680], 6: [730, 690], 5: [740, 700], 4: [750, 720],
          3: [760, 750], 2: [770, 770], 1: [790, 790], 0: [800, 800]}


@login_required(login_url='loginpage')
def processtest(request):
    username = request.user

    try:
        testData = testInProgress.objects.get(studentId=username.id)
        testQuery = testSpec.objects.get(id=testData.testId)
        print(testData.testName, testData.testId)
        print('test status: ', testData.statusReading, testData.statusWriting,
              testData.studentAnswersReading, testData.studentAnswersWriting
              )

    except:
        messages.warning(request, "VIOLATION OF TESTING PROCESS AND/OR CONDITIONS!")
        return redirect('index')

    if (testData.statusReading == 'YES' and testData.statusWriting == 'YES'
        and testData.statusMathOne == 'YES') and testData.statusMathTwo == 'YES':
        correct = []
        inCorrect = []

        correctQtype = []
        wrongQtype = []

        studentAnswersR = testData.studentAnswersReading
        studentAnswersW = testData.studentAnswersWriting
        studentAnswersM1 = testData.studentAnswersMathOne
        studentAnswersM2 = testData.studentAnswersMathTwo

        readingAnswerKey = testQuery.answerKeyReading
        writingAnswerKey = testQuery.answerKeyWriting
        mathOneAnswerKey = testQuery.answerKeyMathOne
        mathTwoAnswerKey = testQuery.answerKeyMathTwo

        readingQT = testQuery.questionTypeReading
        writingQT = testQuery.questionTypeWriting
        mathM1QT = testQuery.questionTypeMathOne
        mathM2QT = testQuery.questionTypeMathTwo

        qTypeTotalR = []
        for k, v in readingQT.items():
            qTypeTotalR.append(v)
        qTypeTotalR = dict(collections.Counter(qTypeTotalR))

        qTypeTotalW = []
        for k, v in writingQT.items():
            qTypeTotalW.append(v)
        qTypeTotalW = dict(collections.Counter(qTypeTotalW))

        qTypeTotalM1 = []
        for k, v in mathM1QT.items():
            qTypeTotalM1.append(v)
        qTypeTotalM1 = dict(collections.Counter(qTypeTotalM1))
        print("qTypeTotalM1", qTypeTotalM1)

        qTypeTotalM2 = []
        for k, v in mathM2QT.items():
            qTypeTotalM2.append(v)
        qTypeTotalM2 = dict(collections.Counter(qTypeTotalM2))

        cleanAnswerR = {}
        cleanAnswerW = {}
        cleanAnswerM1 = {}
        cleanAnswerM2 = {}

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

        for k, v in mathOneAnswerKey.items():
            try:
                cleanAnswerM1[k] = studentAnswersM1[k]
            except:
                cleanAnswerM1[k] = 'X'

        for k, v in mathTwoAnswerKey.items():
            try:
                cleanAnswerM2[k] = studentAnswersM2[k]
            except:
                cleanAnswerM2[k] = 'X'

        studentAnswersR = cleanAnswerR
        studentAnswersW = cleanAnswerW
        studentAnswersM1 = cleanAnswerM1
        studentAnswersM2 = cleanAnswerM2

        # return JsonResponse( cleanAnswerW, safe=False)

        ############## classify question types

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

        inCorrect = []
        wrongQtype = []

        # for x, y in studentAnswersM1.items():
        #     # print(x, y, testQuery.answerKeyReading[x])
        #     if y != mathOneAnswerKey[x]:
        #         inCorrect.append(x)
        #         wrongQtype.append(testQuery.questionTypeMathOne[x])

        for x, y in studentAnswersM1.items():
            if y in mathOneAnswerKey[x]:
                pass
            else:
                inCorrect.append(x)
                wrongQtype.append(testQuery.questionTypeMathOne[x])

        wrongQ = dict(collections.Counter(wrongQtype))
        wrongSortM1 = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
        numberInCorrectM1 = str(len(inCorrect))
        print("Math Section 1: -" + numberInCorrectM1 + ",", wrongSortM1)
        print(wrongQ, wrongSortM1)

        inCorrect = []
        wrongQtype = []

        for x, y in studentAnswersM2.items():
            if y in mathTwoAnswerKey[x]:
                pass
            else:
                inCorrect.append(x)
                wrongQtype.append(testQuery.questionTypeMathTwo[x])

        wrongQ = dict(collections.Counter(wrongQtype))
        wrongSortM2 = dict(sorted(wrongQ.items(), key=lambda item: item[1], reverse=True))
        numberInCorrectM2 = str(len(inCorrect))
        print("Math Section 2: -" + numberInCorrectM2 + ",", wrongSortM2)

        qTypePercentR = {}
        for x, y in qTypeTotalR.items():
            try:
                qTypePercentR[x] = round(100 * ((int(qTypeTotalR[x]) - int(wrongSortR[x])) / int(qTypeTotalR[x])))
            except:
                qTypePercentR[x] = 100
        jsonQtypePerR = dict(sorted(qTypePercentR.items(), key=lambda item: item[1], reverse=True))
        print('R % correct: ', jsonQtypePerR)

        qTypePercentW = {}
        for x, y in qTypeTotalW.items():
            try:
                qTypePercentW[x] = round(100 * ((int(qTypeTotalW[x]) - int(wrongSortW[x])) / int(qTypeTotalW[x])))
            except:
                qTypePercentW[x] = 100
        jsonQtypePerW = dict(sorted(qTypePercentW.items(), key=lambda item: item[1], reverse=True))
        print('W % correct: ', jsonQtypePerW)

        qTypePercentM1 = {}
        for x, y in qTypeTotalM1.items():
            print(x, y)
            try:
                qTypePercentM1[x] = round(100 * ((int(qTypeTotalM1[x]) - int(wrongSortM1[x])) / int(qTypeTotalM1[x])))
                print(round(100 * ((int(qTypeTotalM1[x]) - int(wrongSortM1[x])) / int(qTypeTotalM1[x]))))
            except:
                qTypePercentM1[x] = 100
        jsonQtypePerM1 = dict(sorted(qTypePercentM1.items(), key=lambda item: item[1], reverse=True))
        print('m1 % correct: ', jsonQtypePerM1)

        qTypePercentM2 = {}
        for x, y in qTypeTotalM2.items():
            try:
                qTypePercentM2[x] = round(100 * ((int(qTypeTotalM2[x]) - int(wrongSortM2[x])) / int(qTypeTotalM2[x])))
            except:
                qTypePercentM2[x] = 100
        jsonQtypePerM2 = dict(sorted(qTypePercentM2.items(), key=lambda item: item[1], reverse=True))
        print('m2 % correct: ', jsonQtypePerM2)

        # save for correct number of questions conversion
        # rawVerbal = 66 - (int(numberInCorrectR) + int(numberInCorrectW))
        # rawMath = 54 - (int(numberInCorrectM1) + int(numberInCorrectM2))

        # verbalKeyLen = len(testQuery.answerKeyReading) + len(testQuery.answerKeyWriting)
        # mathKeyLen = len(testQuery.answerKeyMathOne) + len(testQuery.answerKeyMathTwo)
        #
        # rawVerbal = verbalKeyLen - (int(numberInCorrectR) + int(numberInCorrectW))
        # rawMath = mathKeyLen - (int(numberInCorrectM1) + int(numberInCorrectM2))

        rawVerbal = (int(numberInCorrectR) + int(numberInCorrectW))
        rawMath = (int(numberInCorrectM1) + int(numberInCorrectM2))

        readingscore = newraw[rawVerbal][0]
        mathscore = newraw[rawMath][1]

        print(rawVerbal, rawMath, readingscore, mathscore)

        r = testRecord.objects.create(studentUsername=username.username,
                                      studentName=username.first_name,
                                      testName=testData.testName,
                                      testId=testData.testId,
                                      studentAnswersReading=studentAnswersR,
                                      studentAnswersWriting=studentAnswersW,
                                      studentAnswersMathOne=studentAnswersM1,
                                      studentAnswersMathTwo=studentAnswersM2,
                                      numberInCorrectR=numberInCorrectR,
                                      numberInCorrectW=numberInCorrectW,
                                      numberInCorrectM1=numberInCorrectM1,
                                      numberInCorrectM2=numberInCorrectM2,
                                      jsonWrongQtypeR=wrongSortR,
                                      jsonWrongQtypeW=wrongSortW,
                                      jsonWrongQtypeMathOne=wrongSortM1,
                                      jsonWrongQtypeMathTwo=wrongSortM2,
                                      jsonQtypePerR=jsonQtypePerR,
                                      jsonQtypePerW=jsonQtypePerW,
                                      jsonQtypePerMathOne=jsonQtypePerM1,
                                      jsonQtypePerMathTwo=jsonQtypePerM2,
                                      scoreReading=readingscore,
                                      scoreMath=mathscore
                                      )

        # print('record saved: ', r)

        # testData.delete()

        # return render(request, 'cbtsystem/processTest.html', {"testData": testData, "testQuery": testQuery})
        return redirect('index')
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

    ptest = {
        0: [200, 200],
        1: [210, 220],
        2: [220, 230],
        3: [230, 240],
        4: [240, 250],
        5: [250, 280],
        6: [260, 300],
        7: [270, 320],
        8: [280, 340],
        9: [290, 350],
        10: [300, 360],
        11: [310, 380],
        12: [330, 390],
        13: [340, 400],
        14: [350, 410],
        15: [360, 430],
        16: [380, 440],
        17: [390, 450],
        18: [400, 460],
        19: [410, 480],
        20: [430, 490],
        21: [440, 500],
        22: [460, 510],
        23: [470, 520],
        24: [490, 530],
        25: [500, 540],
        26: [510, 550],
        27: [520, 560],
        28: [530, 570],
        29: [540, 580],
        30: [550, 590],
        31: [560, 600],
        32: [570, 610],
        33: [580, 620],
        34: [590, 630],
        35: [600, 650],
        36: [610, 660],
        37: [620, 680],
        38: [630, 690],
        39: [640, 700],
        40: [650, 720],
        41: [660, 750],
        42: [670, 770],
        43: [680, 790],
        44: [690, 800],
        45: [700, "None0"],
        46: [710, "None0"],
        47: [720, "None0"],
        48: [730, "None0"],
        49: [740, "None0"],
        50: [750, "None0"],
        51: [760, "None0"],
        52: [770, "None0"],
        53: [790, "None0"],
        54: [800, "None0"]
    }

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

    for k, v in newraw.items():
        raw.append(k)
        reading.append(v[0])
        writing.append(v[1])

    moo = zip(raw, reading, writing)

    for k, v in topper.items():
        topscore.append(k)
        topverbal.append(v[0])
        topmath.append(v[1])

    foo = zip(topscore, topverbal, topmath)

    return render(request, 'cbtsystem/rawscale.html', {'moo': moo, 'foo': foo})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        refcode = request.POST.get("code", "")
        refcode = refcode.strip()
        # print(groupType)
        if form.is_valid():
            user = form.save()
            accountprofile.objects.create(userAccount=user, school=refcode)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created: {username}')

            return redirect('loginpage')

    else:
        form = UserRegisterForm()

    return render(request, 'cbtsystem/register.html', {'form': form})
