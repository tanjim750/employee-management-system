import csv
from django.http import HttpResponse
from app.models import attendance,DateTimeNow
import time
from datetime import datetime

def download_todays_attendance_sheet(request):
    # Query all employees from the database
    date_time_now = DateTimeNow.objects.create()
    todayAttendance = attendance.objects.filter(day=date_time_now.date)

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="todays_attendance_sheet.csv"'

    # Create the CSV writer and write the header
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Number', 'In Time', 'Working Period', 'Out Time', 'Early In', 'Late In', 'Early Out','Late In'])


    # Write the employee data to the CSV
    for attd in todayAttendance:
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

            writer.writerow([f"{attd.user.first_name} {attd.user.last_name}", attd.user.email, attd.user.employee.number, str(attd.check_in.time().strftime("%I:%M:%S")).split(".")[0], workingPeriod, checkOut, earlyIn,lateIn,earlyOut,lateOut])


    # Set a cookie to indicate successful download
    response.set_cookie('downloaded', 'true', max_age=5)

    time.sleep(3)
    return response


