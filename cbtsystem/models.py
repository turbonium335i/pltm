from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import datetime, timedelta
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
    pdfLink = models.URLField(max_length=250, null=True, blank=True,
                              default="https://drive.google.com/file/d/14xUAfhLiG2AQR-jdNcjwT9ZYlA0ZaHZr/preview")
    pdfLink2 = models.URLField(max_length=250, null=True, blank=True,
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
    studentFlagReading = JSONField(null=True, default={})
    studentFlagWriting = JSONField(null=True, default={})
    statusReading = models.CharField(max_length=3, null=True, blank=True, default='NO')
    statusWriting = models.CharField(max_length=3, null=True, blank=True, default='NO')
    timeLeftReading = models.CharField(max_length=200, null=True, blank=True, default='60')
    timeLeftWriting = models.CharField(max_length=200, null=True, blank=True, default='60')

    def __str__(self):
        return '{0} {1} {2} {3} {4}'.format(self.id, self.testName, self.date_started.strftime("%m/%d/%Y %H:%M:%S"),  self.studentUsername, self.studentName)


class testRecord(models.Model):
    studentUsername = models.CharField(null=True, blank=False, max_length=200)
    studentName = models.CharField(null=True, blank=False, max_length=200)
    testName = models.CharField(max_length=200, null=True, blank=True)
    testId = models.CharField(max_length=100, null=True, blank=True)
    date_finished = models.DateTimeField(auto_now_add=True)
    studentAnswersReading = JSONField(null=True, default={})
    studentAnswersWriting = JSONField(null=True, default={})
    numberInCorrectR = models.CharField(max_length=10, null=True, default='0')
    numberInCorrectW = models.CharField(max_length=10, null=True, default='0')
    scoreReading = models.CharField(max_length=3, null=True, default='200')
    scoreWriting = models.CharField(max_length=3, null=True, default='200')
    jsonWrongQtypeR = JSONField(null=True, default={})
    jsonWrongQtypeW = JSONField(null=True, default={})


    def __str__(self):
        return '{0} {1} {2} {3} {4}'.format(self.id, self.testName, self.date_finished.strftime("%m/%d/%Y %H:%M:%S"),  self.studentUsername, self.studentName)


class groupTest(models.Model):

    showTest = models.ManyToManyField(testSpec, blank=True)

    def __str__(self):
        return "Test Group"
