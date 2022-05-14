from django.contrib import admin
from .models import *


class testRecordAdmin(admin.ModelAdmin):
    search_fields = ('studentUsername', 'studentName', 'testName', 'date_finished')

class testSpecAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', 'notes')

# admin.site.register(testRecord)
admin.site.register(testInProgress)
admin.site.register(groupTest)

#custom search functions
admin.site.register(testRecord, testRecordAdmin)
admin.site.register(testSpec, testSpecAdmin)
