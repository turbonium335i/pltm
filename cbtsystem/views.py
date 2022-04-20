from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):

    return render(request, 'cbtsystem/index.html' )

def demo(request):

    return render(request, 'cbtsystem/demo.html' )
