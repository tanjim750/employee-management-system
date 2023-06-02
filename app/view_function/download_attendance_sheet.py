import csv
from django.http import HttpResponse
from app.models import attendance , DateTimeNow
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Q
import time
from datetime import datetime


def download_attendance_sheet(request):
    username = request.GET.get("e",None)
    day1 = request.GET.get("day1",None)
    day2 = request.GET.get("day2",None)
    month1 = request.GET.get("month1",None)
    month2 = request.GET.get("month2",None)
    year1 = request.GET.get("year1",None)
    year2 = request.GET.get("year2",None)

    if username != None and day1 != None and day2 != None and month1 != None and month2 != None and year1 != None and year2 != None:
        user = User.objects.get(username=username)

        current_year = now().year

        if year1 != "all" and year2 != "None" :
            if int(year1) > int(year2):
                lteYear = int(year1)
                gteYear = int(year2)
            else:
                lteYear = int(year2)
                gteYear = int(year1)
        elif year1 != "all" and year2 == "None":
            lteYear = int(year1)
            gteYear = int(year1)
        elif year1 == "all":
            gteYear = 1
            lteYear = current_year
        
        if month1 != "all" and month2 != "None" :
            if int(month1) > int(month2):
                lteMonth = int(month1)
                gteMonth = int(month2)
            else:
                lteMonth = int(month2)
                gteMonth = int(month1)
        elif month1 != "all" and month2 == "None":
            lteMonth = int(month1)
            gteMonth = int(month1)
        elif month1 == "all":
            gteMonth = 1
            lteMonth = 12

        
        if day1 != "all" and day2 != "None" :
            if int(day1) > int(day2):
                lteDay = int(day1)
                gteDay = int(day2)
            else:
                lteDay = int(day2)
                gteDay = int(day1)
        elif day1 != "all" and day2 == "None":
            lteDay = int(day1)
            gteDay = int(day1)
        elif day1 == "all":
            gteDay = 1
            lteDay = 31


        # filter system
        _attendance = attendance.objects.filter(Q(day__day__gte = int(gteDay)) & Q(day__day__lte = int(lteDay)) & Q(day__month__gte = int(gteMonth)) & Q(day__month__lte = int(lteMonth)) & Q(day__year__gte = gteYear) & Q(day__year__lte = lteYear) & Q(user=user))

        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employee-attendance-sheet.csv"'

        # Create the CSV writer and write the headeruser
        writer = csv.writer(response)
        writer.writerow(['Date','Name', 'Email', 'Number', 'In Time', 'Working Period', 'Out Time', 'Early In', 'Late In', 'Early Out','Late In'])

        # Write the employee data to the CSV
        for attd in _attendance:
            if attd.attend:
                workingPeriod = str(attd.working_period)

                checkOut = str(attd.check_out.time().strftime("%I:%M:%S")).split(".")[0]

                if attd.early_out:
                    earlyOut = str(attd.early_out).split(".")[0]
                else:
                    earlyOut = "No"
                
                if attd.late_out:
                    lateOut = str(attd.late_out).split(".")[0]
                else:
                    lateOut = "No"
                
                
            else:
                checkOut = "Working"
                earlyOut = "---"
                lateOut = "---"

                nowTime = DateTimeNow.objects.create()
    
                workingPeriod = datetime.combine(nowTime.date,nowTime.time) - datetime.combine(nowTime.date,attd.check_in.time())
                total_seconds = datetime.fromtimestamp(workingPeriod.total_seconds())
                workingPeriod = str(total_seconds.strftime("%H:%M:%S"))

            workingPeriod = workingPeriod.split(".")[0]

            if attd.early_in:
                earlyIn = str(attd.early_in).split(".")[0]
            else:
                earlyIn = "No"
            
            if attd.late_in:
                lateIn = str(attd.late_in).split(".")[0]
            else:
                lateIn = "No"

            writer.writerow([attd.day ,f"{user.first_name} {user.last_name}", user.email, user.employee.number, str(attd.check_in.time().strftime("%I:%M:%S")).split(".")[0], workingPeriod, checkOut, earlyIn,lateIn,earlyOut,lateOut])

        # Set a cookie to indicate successful download
        response.set_cookie('downloaded', 'true', max_age=5)

        time.sleep(3)
        return response