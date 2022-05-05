from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('demo', views.demo, name='demo'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('logoutpage', views.logoutpage, name='logoutpage'),
    path('breakpage', views.breakPage, name='breakpage'),
    path('directions', views.directions, name='directions'),
    path('results', views.results, name='results'),
    path('endsection', views.endsection, name='endsection'),
    path('processtest', views.processtest, name='processtest'),




]

