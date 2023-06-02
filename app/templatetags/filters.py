from django.template import Library
from app.models import *
from datetime import datetime , timedelta
register = Library()

justTime = AttendanceTimeLimit.objects.get(id=1)
today = datetime.today()
dateTimeNow = DateTimeNow.objects.create()

@register.filter
def getTime(checkIn , action):
    if action == "early":
        if checkIn.time() < justTime.JustInTime:
            early_in = (datetime.combine(dateTimeNow.date,justTime.JustInTime) - datetime.combine(dateTimeNow.date,checkIn.time()))
            return datetime.strptime(str(early_in),"%H:%M:%S.%f")
        else:
            return ("---")
        print(type(checkIn.time()),type(justTime.JustInTime))
    elif action == "late":
        if checkIn.time() > justTime.JustInTime:
            late_in = (datetime.combine(dateTimeNow.date,checkIn.time()) - datetime.combine(dateTimeNow.date,justTime.JustInTime))
            return datetime.strptime(str(late_in),"%H:%M:%S.%f")
        else:
            return ("---")
        print(type(checkIn.time()),type(justTime.JustInTime))

@register.filter
def liveTimeCount(check_in,now=None):    
    working_time = datetime.combine(dateTimeNow.date,dateTimeNow.time) - datetime.combine(dateTimeNow.date,check_in.time())
    total_seconds = datetime.fromtimestamp(working_time.total_seconds())
    return str(total_seconds.strftime("%I:%M:%S"))

@register.filter
def getMonth(currentIndex,List):
    currentIndex = int(currentIndex)
    if currentIndex > 0:
        currentDate = List[currentIndex]["day"]
        previousDate = List[currentIndex -1]["day"]

        if (currentDate.month != previousDate.month) or (currentDate.year != previousDate.year) :
            return True
        else:
            return False
    else:
        return False
    

@register.filter
def last_leave(instance,agr=None):
    user = instance.user
    lastLeave = leaveApplication.objects.filter(date=dateTimeNow.date,user=user,approved=True)
    if lastLeave.exists():
        return lastLeave.last().date
    else:
        return 'None'

@register.filter
def total_leave_requests(instance,arg=None):
    user = instance.user
    total_requests = leaveApplication.objects.filter(date=dateTimeNow.date,user=user)
    return total_requests.count()

@register.filter
def total_approved(instance,arg=None):
    user = instance.user
    approved = leaveApplication.objects.filter(date=dateTimeNow.date,user=user,approved=True)
    return approved.count()

@register.filter
def leave_request_update(leave_from,leave_to):
    if leave_to == "rejected":
        message = "You have requested for leave but sorry we cannot consider this. You can meet with management."
    else:
        if leave_to and (leave_to - leave_from).days > 1:
            message = f"You have requested for leave and it's approved for {(leave_to - leave_from).days} days from {leave_from} to {leave_to}. You have to continue from {leave_to+timedelta(days=1)}.\n\n"
        else:
            message = f"You have requested for leave and it's approved for 1 day date is {leave_from}. You have to continue from {leave_from+timedelta(days=1)}.\n\n"
        
    return message