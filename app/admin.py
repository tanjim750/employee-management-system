from django.contrib import admin
from .models import *

admin.site.register(employee)
admin.site.register(attendance)
admin.site.register(DateTimeNow)
admin.site.register(AttendanceTimeLimit)
admin.site.register(holiday)
admin.site.register(leaveApplication)