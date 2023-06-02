from django.shortcuts import render , redirect
from django.http import HttpResponse , Http404, JsonResponse
import calendar
from app.models import *
from django.utils.timezone import now
from django.db.models import Q
import requests
from datetime import datetime, timedelta

def check_attendance(request):
    context = {}
    context["check_attendance_page"] = True
    _DateTimeNow = DateTimeNow.objects.create()
    username = request.GET.get("e",None)
    if username is not None:
        user = User.objects.get(username=username)
        current_month = now().month
        current_year = now().year

        days_range = calendar.monthrange(current_year,current_month)
        days = [ str(num) for num in range(days_range[0]+1,days_range[1]+1)]
        months = [{"month":"Jan","value":"1"},{"month":"Feb","value":"2"},{"month":"Mar","value":"3"},{"month":"Apr","value":"4"},
                {"month":"May","value":"5"},{"month":"June","value":"6"},{"month":"July","value":"7"},{"month":"Aug","value":"8"},
                {"month":"Sep","value":"9"},{"month":"Oct","value":"10"},{"month":"Nov","value":"11"},{"month":"Dec","value":"12"}]
        joined_year = user.date_joined.year
        years = [str(year) for year in range(joined_year,current_year+1)]
        context["user"] = user
        context["days"] = days
        context["months"] = months
        context["default_month1"] = str(current_month)
        context["years"] = years
        context["default_year1"] = str(current_year)

        # manage post request
        if request.method == "POST":
            day1 = request.POST['day1']
            day2 = request.POST['day2']
            month1 = request.POST['month1']
            month2 = request.POST['month2']
            year1 = request.POST['year1']
            year2 = request.POST['year2']

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
                gteYear = joined_year
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

            # count total working days
            total_holidays = holiday.objects.filter(Q(date__day__gte = int(gteDay)) & Q(date__day__lte = int(lteDay)) & Q(date__month__gte = int(gteMonth)) & Q(date__month__lte = int(lteMonth)) & Q(date__year__gte = gteYear) & Q(date__year__lte = lteYear)).count()
            try:
                if day1 == "all" and month1 == "all" and int(year1) == current_year:
                    total_days = (datetime(current_year,current_month,now().day) - datetime(current_year,1,1)).days + 1
                    total_holidays = holiday.objects.filter(Q(date__day__gte = int(1)) & Q(date__day__lte = 31) & Q(date__month__gte = 1) & Q(date__month__lte = int(current_month)) & Q(date__year = current_year)).count()
                else:
                    total_days = (datetime(lteYear,lteMonth,lteDay) - datetime(gteYear,gteMonth,gteDay)).days + 1
            except:
                total_days = (datetime(lteYear,lteMonth, 28 if lteMonth == 2 else 30 ) - datetime(gteYear,gteMonth, gteDay)).days + 1

            total_working_days = total_days - total_holidays
            context['total_working_days'] = total_working_days

            context["default_day1"] = day1
            context["default_month1"] = month1
            context["default_day2"] = day2
            context["default_month2"] = month2
            context["default_year1"] = year1
            context["default_year2"] = year2
            # context["attendances"] = _attendance
        else:
            _attendance = attendance.objects.filter(Q(day__year = int(current_year)) & Q(day__month = int(current_month)) & Q(user=user)).order_by("day")
            # count total working days 
            total_days = (datetime(current_year,current_month,now().day) - datetime(current_year,current_month,1)).days + 1
            total_holidays = holiday.objects.filter(Q(date__year = int(current_year)) & Q(date__month = int(current_month))).count()
            total_working_days = total_days - total_holidays
            context['total_working_days'] = total_working_days
            # context["attendances"] = _attendance
        _AttendanceTimeLimit = AttendanceTimeLimit.objects.get(id=1)

        context['total_attendance'] = _attendance.count()

        # make employee attendance list 
        attendance_list = []
        month_start_with = 1
        previous_Attd_month = None
        previous_Attd_year = None
        for Attd in _attendance:
            current_Attd_month = Attd.day.month
            current_Attd_year = Attd.day.year

            if current_Attd_month == current_month and current_Attd_year == current_year:
                month_ends_with = now().day
            else:
                days_in_month = calendar.monthrange(current_Attd_year,current_Attd_month)
                month_ends_with = days_in_month[1]

            if current_Attd_month == previous_Attd_month and current_Attd_year == previous_Attd_year:
                day = month_start_with
            else:
                day = 1

            previous_Attd_month = current_Attd_month
            previous_Attd_year = current_Attd_year
            run_loop = True
            while run_loop:
                attd_dict = {}
                date = datetime(current_Attd_year,current_Attd_month,day).date()
                Attd_exist = _attendance.filter(day=date)
                day += 1
                month_start_with = day
                if Attd.day == date:
                    attd_dict["status"] = "present"
                    attd_dict["day"] = Attd.day
                    attd_dict["check_in"] = Attd.check_in
                    attd_dict["check_out"] = Attd.check_out
                    attd_dict["working_period"] = Attd.working_period
                    attd_dict["early_in"] = Attd.early_in
                    attd_dict["early_out"] = Attd.early_out
                    attd_dict["late_in"] = Attd.late_in
                    attd_dict["late_out"] = Attd.late_out

                    if Attd.attend:
                        attd_dict["attend"] = True
                    else:
                        attd_dict["attend"] = False

                    attendance_list.append(attd_dict)

                elif not Attd_exist.exists():
                    check_holiday = holiday.objects.filter(date=date)
                    if check_holiday.exists():
                        attd_dict["status"] = "holiday"
                        attd_dict["day"] = date
                        attd_dict["name"] = check_holiday.first().name
                    else:
                        attd_dict["status"] = "absent"
                        attd_dict["day"] = date

                    attendance_list.append(attd_dict)
                
                
                if Attd_exist.exists() or Attd.day == date or day == month_ends_with:
                    run_loop = False


        context["attendances"] = attendance_list
        # print(attendance_list)
        # return JsonResponse(attendance_list,safe=False)

        # count total early and late time 
        earlyInHours = 0
        earlyInMinutes = 0
        lateInHours = 0
        lateInMinutes = 0
        earlyOutHours = 0
        earlyOutMinutes = 0
        lateOutHours = 0
        lateOutMinutes = 0
        for attd in _attendance:
            if attd.early_in:
                earlyIn = str(attd.early_in).split(":")
                earlyInHours += int(earlyIn[0])
                earlyInMinutes += int(earlyIn[1])
            if attd.late_in:
                lateIn = str(attd.late_in).split(":")
                lateInHours += int(lateIn[0])
                lateInMinutes += int(lateIn[1])
            if attd.early_out:
                earlyOut = str(attd.early_out).split(":")
                earlyOutHours += int(earlyOut[0])
                earlyOutMinutes += int(earlyOut[1])
            if attd.late_out:
                lateOut = str(attd.late_out).split(":")
                lateOutHours += int(lateOut[0])
                lateOutMinutes += int(lateOut[1])

        totalEarlyInTime = str(earlyInHours)+" Hours"+" "+str(earlyInMinutes)+" Mins"
        totalLateInTime = str(lateInHours)+" Hours"+" "+str(lateInMinutes)+" Mins"
        totalEarlyOutTime = str(earlyOutHours)+" Hours"+" "+str(earlyOutMinutes)+" Mins"
        totalLateOutTime = str(lateOutHours)+" Hours"+" "+str(lateOutMinutes)+" Mins"

        context['totalEarlyInTime'] = totalEarlyInTime
        context['totalLateInTime'] = totalLateInTime
        context['totalEarlyOutTime'] = totalEarlyOutTime
        context['totalLateOutTime'] = totalLateOutTime

        
        
    else:
        return HttpResponse("Invalid Request", Http404)

    return render(request,"secondery/attendance.html",context)