from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class testRecordAdmin(admin.ModelAdmin):
    search_fields = ('studentUsername', 'studentName', 'testName', 'date_finished')

class testSpecAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', 'notes')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# admin.site.register(testRecord)
admin.site.register(testInProgress)
admin.site.register(groupTest)
admin.site.register(LoggedInUser)
admin.site.register(QtypeNote)


#custom search functions
admin.site.register(testRecord, testRecordAdmin)
admin.site.register(testSpec, testSpecAdmin)
