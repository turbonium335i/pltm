from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session

from django.conf import settings
from jsonfield import JSONField


class testSpec(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    answerKeyReading = JSONField(null=True, default={})
    questionTypeReading = JSONField(null=True, default={})

    answerKeyWriting = JSONField(null=True, default={})
    questionTypeWriting = JSONField(null=True, default={})

    answerKeyMathOne = JSONField(null=True, default={})
    questionTypeMathOne = JSONField(null=True, default={})
    studentResponseOne = models.TextField(null=True, blank=True, default="12")

    answerKeyMathTwo = JSONField(null=True, default={})
    questionTypeMathTwo = JSONField(null=True, default={})
    studentResponseTwo = models.TextField(null=True, blank=True, default="12")

    pdfLink = models.URLField(max_length=250, null=True, blank=True,
                              default="https://drive.google.com/file/d/14xUAfhLiG2AQR-jdNcjwT9ZYlA0ZaHZr/preview")
    pdfLink2 = models.URLField(max_length=250, null=True, blank=True,
                               default="https://drive.google.com/file/d/14xUAfhLiG2AQR-jdNcjwT9ZYlA0ZaHZr/preview")
    pdfLinkMathOne = models.URLField(max_length=250, null=True, blank=True,
                               default="https://drive.google.com/file/d/14xUAfhLiG2AQR-jdNcjwT9ZYlA0ZaHZr/preview")
    pdfLinkMathTwo = models.URLField(max_length=250, null=True, blank=True,
                               default="https://drive.google.com/file/d/14xUAfhLiG2AQR-jdNcjwT9ZYlA0ZaHZr/preview")

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.id, self.name, self.notes)


class testInProgress(models.Model):
    studentId = models.CharField(null=True, blank=False, max_length=7)
    studentUsername = models.CharField(null=True, blank=False, max_length=200)
    studentName = models.CharField(null=True, blank=False, max_length=200)
    testName = models.CharField(max_length=200, null=True, blank=True)
    testId = models.CharField(max_length=100, null=True, blank=True)
    date_started = models.DateTimeField(auto_now_add=True)
    studentAnswersReading = JSONField(null=True, default={})
    studentAnswersWriting = JSONField(null=True, default={})
    studentAnswersMathOne = JSONField(null=True, default={})
    studentAnswersMathTwo = JSONField(null=True, default={})
    studentFlagReading = JSONField(null=True, blank=True, default={})
    studentFlagWriting = JSONField(null=True, blank=True, default={})
    studentFlagMathOne = JSONField(null=True, blank=True, default={})
    studentFlagMathTwo = JSONField(null=True, blank=True, default={})
    statusReading = models.CharField(max_length=3, null=True, blank=True, default='NO')
    statusWriting = models.CharField(max_length=3, null=True, blank=True, default='NO')
    statusMathOne = models.CharField(max_length=3, null=True, blank=True, default='NO')
    statusMathTwo = models.CharField(max_length=3, null=True, blank=True, default='NO')
    timeLeftReading = models.CharField(max_length=200, null=True, blank=True, default='3610000')
    timeLeftWriting = models.CharField(max_length=200, null=True, blank=True, default='3610000')
    timeLeftMathOne = models.CharField(max_length=200, null=True, blank=True, default='3610000')
    timeLeftMathTwo = models.CharField(max_length=200, null=True, blank=True, default='3610000')

    def __str__(self):
        return '{0} {1} {2} {3} {4}'.format(self.id, self.testName, self.date_started.strftime("%m/%d/%Y %H:%M:%S"),
                                            self.studentUsername, self.studentName)


class testRecord(models.Model):
    studentUsername = models.CharField(null=True, blank=False, max_length=200)
    studentName = models.CharField(null=True, blank=False, max_length=200)
    testName = models.CharField(max_length=200, null=True, blank=True)
    testId = models.CharField(max_length=100, null=True, blank=True)
    date_finished = models.DateTimeField(auto_now_add=True)
    studentAnswersReading = JSONField(null=True, default={})
    studentAnswersWriting = JSONField(null=True, default={})
    studentAnswersMathOne = JSONField(null=True, default={})
    studentAnswersMathTwo = JSONField(null=True, default={})
    numberInCorrectR = models.CharField(max_length=10, null=True, default='0')
    numberInCorrectW = models.CharField(max_length=10, null=True, default='0')
    numberInCorrectM1 = models.CharField(max_length=10, null=True, default='0')
    numberInCorrectM2 = models.CharField(max_length=10, null=True, default='0')
    scoreReading = models.CharField(max_length=3, null=True, default='200')
    scoreWriting = models.CharField(max_length=3, null=True, default='200')
    scoreMath = models.CharField(max_length=3, null=True, default='200')
    jsonWrongQtypeR = JSONField(null=True, default={})
    jsonWrongQtypeW = JSONField(null=True, default={})
    jsonQtypePerR = JSONField(null=True, default={})
    jsonQtypePerW = JSONField(null=True, default={})
    jsonWrongQtypeMathOne = JSONField(null=True, default={})
    jsonWrongQtypeMathTwo = JSONField(null=True, default={})
    jsonQtypePerMathOne = JSONField(null=True, default={})
    jsonQtypePerMathTwo = JSONField(null=True, default={})

    def total(self):
        return int(self.scoreReading) + int(self.scoreMath)

    def __str__(self):
        return '{0} {1} {2} {3} {4} V1:-{5} V2:-{6} M1:-{7} M2:-{8}, [ R{9}, M{10} ]'.format(self.id, self.testName,
                                                          self.date_finished.strftime("%m/%d/%Y %H:%M:%S"),
                                                          self.studentUsername, self.studentName, self.numberInCorrectR,
                                                          self.numberInCorrectW, self.numberInCorrectM1, self.numberInCorrectM2,
                                                          self.scoreReading, self.scoreMath)


class groupTest(models.Model):
    showTest = models.ManyToManyField(testSpec, blank=True)

    def __str__(self):
        return "Test Group"


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username


class loggrecord(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    logdate = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.username, self.logdate)

class QtypeNote(models.Model):

    title = models.CharField(max_length=100, null=True, default='QtypeNotes Title')
    notes = models.TextField(null=True, blank=True, default='QtypeNotes Notes')

    def __str__(self):
        return 'id: {0} - {1} '.format(self.id, self.title)

class testDate(models.Model):

    next_test = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return 'id: {0} - {1} '.format(self.id, self.next_test)

S_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class accountprofile(models.Model):
    userAccount = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    signupdate = models.DateTimeField(default=datetime.now, blank=True)
    school = models.CharField(max_length=100, null=True, default='School Name')
    age = models.PositiveIntegerField(null=True, blank=True, default=16)
    sex = models.CharField(max_length=100, null=True, choices=S_TYPE, blank=True)
    allowed = models.ManyToManyField(testSpec, blank=True)

    comment = models.TextField(null=True, blank=True,
                             default="Write comments here.")

    def __str__(self):
        return '{0} / {1}, {2} / School: {3} / STATUS: {4}'.format(self.userAccount, self.userAccount.first_name, self.userAccount.last_name, self.school, self.status)


