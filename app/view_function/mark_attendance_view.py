from django.shortcuts import render, redirect
from app.models import *
from django.utils.timezone import now
from datetime import datetime

def mark_attendance(request):
    dateTimeNow = DateTimeNow.objects.create()
    already_checkedIn = attendance.objects.filter(user=request.user, day=dateTimeNow.date)
    justTime = AttendanceTimeLimit.objects.get(id=1)

    if request.POST["action"] == "enter":
        checkInTime = dateTimeNow.dateTime

        if not already_checkedIn.exists():
            Attendance = attendance.objects.create(
                user = request.user,
                check_in = checkInTime
            )
            if dateTimeNow.time < justTime.JustInTime:
                earlyIntime = datetime.combine(dateTimeNow.date,justTime.JustInTime) - datetime.combine(dateTimeNow.date,dateTimeNow.time)
                Attendance.early_in = str(earlyIntime)
                Attendance.save()
            else:
                lateInTime = datetime.combine(dateTimeNow.date,dateTimeNow.time) - datetime.combine(dateTimeNow.date,justTime.JustInTime)
                Attendance.late_in = str(lateInTime)
                Attendance.save()

            

    elif request.POST["action"] == "out":

        if already_checkedIn.exists():
            instance = already_checkedIn.first()
            if dateTimeNow.date == instance.check_in.date():
                checkOutTime = dateTimeNow.dateTime

                if dateTimeNow.time < justTime.JustOutTime:
                    earlyOutTime = datetime.combine(dateTimeNow.date,justTime.JustOutTime) - datetime.combine(dateTimeNow.date,dateTimeNow.time)
                    instance.early_out = str(earlyOutTime)
                else:
                    lateOutTime = datetime.combine(dateTimeNow.date,dateTimeNow.time) - datetime.combine(dateTimeNow.date,justTime.JustOutTime)
                    instance.late_out = str(lateOutTime)

                instance.check_out = checkOutTime
                instance.attend = True
                instance.working_period = str(instance.check_out - instance.check_in)
                
                
                instance.save()

                if instance.attend:
                    update_attd = request.user.employee
                    update_attd.total_attd = attendance.objects.filter(user=request.user, attend=True).count()
                    update_attd.save()

                    
            
    return redirect("index")