from django.shortcuts import render
from app.models import *
from django.db.models import Q
def todays_attendance_view(request):
    context = {}
    date_time_now = DateTimeNow.objects.create()
    query = request.GET.get('q', None)
    if query is not None:
        _attendance =attendance.objects.filter(
                Q(day=date_time_now.date) & 
                (Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) |
                Q(user__email__icontains=query) |
                Q(user__employee__position__icontains = query))
            )
    else:
        _attendance = attendance.objects.filter(day=date_time_now.date).order_by("-id")
    context['todays_attendance_page'] = True
    context["attendances"]= _attendance

    if request.method == 'POST':
        application = request.POST['application']
        context['application'] = application
    return render(request,'secondery/todays_attendance.html',context)