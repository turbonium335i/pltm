from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import *
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))
    # loggrecord.objects.create(username=kwargs.get('user'), logdate=formatedDate)

@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()

