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
    path('pendingapi', views.pendingTestApi, name='pendingapi'),
    path('cbtreading_pk/<str:pk>', views.cbtreading, name='cbtreading_pk'),
    path('cbtwriting_pk/<str:pk>', views.cbtwriting, name='cbtwriting_pk'),
    path('cbtmathone_pk/<str:pk>', views.cbtmathone, name='cbtmathone_pk'),
    path('cbtmathtwo_pk/<str:pk>', views.cbtmathtwo, name='cbtmathtwo_pk'),
    path('rawscale', views.rawscale, name='rawscale'),
    path('directionsm1', views.directionsm1, name='directionsm1'),
    path('directionsm2', views.directionsm2, name='directionsm2'),
    path('register', views.register, name='register'),
    path('staff', views.staff, name='staff'),
    path('update', views.update, name='update'),

]

