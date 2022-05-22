from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class OneSessionPerUser:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            try:
                current_session_key = request.user.logged_in_user.session_key
                print(current_session_key)
                print(request.session.session_key)

                if current_session_key and current_session_key != request.session.session_key:
                    try:
                        Session.objects.get(session_key=current_session_key).delete()
                    except:
                        request.user.logged_in_user.session_key = request.session.session_key
                        request.user.logged_in_user.save()

                request.user.logged_in_user.session_key = request.session.session_key
                request.user.logged_in_user.save()
            except:
                logout(request)
                messages.info(request, "Authentication Error")
                return redirect('loginpage')

        else:
            print('no session')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response