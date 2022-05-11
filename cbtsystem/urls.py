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
    path('directions2', views.directions2, name='directions2'),
    path('results', views.results, name='results'),
    path('endsection', views.endsection, name='endsection'),
    path('processtest', views.processtest, name='processtest'),
    path('cbtwriting', views.cbtwriting, name='cbtwriting'),
    path('history', views.history, name='history'),
    path('results_pk/<str:pk>', views.results_pk, name='results_pk'),




]

