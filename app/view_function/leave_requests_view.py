from django.shortcuts import render
from django.contrib.auth.models import User
from app.models import *
from django.conf import settings
from datetime import timedelta, datetime, date
#For Send html template to email
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def send_mail(user_email,Subject,admin_message):
    subject = Subject
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email, ]
    html_template = render_to_string('email_template/leave_request.html',{'title':subject, 'application':admin_message})
    message = strip_tags(html_template)
    email = EmailMultiAlternatives(
            subject,
            message,
            email_from,
            recipient_list
    )
    email.attach_alternative(html_template, 'text/html')
    email.send()
    


def reject(request):
    if request.method == "POST":
        if request.POST['action'] == 'reject':
            id = request.POST['id']
            instance = leaveApplication.objects.get(id=id)
            if request.POST['message'] != "":
                instance.admin_message = request.POST['message']
            instance.rejected = True
            instance.checked_on = datetime.today()
            instance.save()

            # send mail that user's leave request rejected
            user_email = instance.user.email
            subject = "Your leave request is rejected"
            message = f"Dear {instance.user.first_name},\nYou have requested for leave but sorry we cannot consider this. You can meet with management.\n\n{request.POST['message']}"
            send_mail(user_email,subject,message)

def approve(request):
    if request.method == "POST":
        if request.POST['action'] == 'approve':
            id = request.POST['id']
            instance = leaveApplication.objects.get(id=id)
            starting_date = (request.POST['startingDate']).split("-")
            starting_date_year = int(starting_date[0])
            starting_date_month = int(starting_date[1])
            starting_date_day = int(starting_date[2])
            leave_from = date(starting_date_year,starting_date_month,starting_date_day)
            instance.leave_from = leave_from

            if request.POST['message'] != "":
                instance.admin_message = request.POST['message']
            if request.POST['endingDate'] != "":
                ending_date = (request.POST['endingDate']).split("-")
                ending_date_year = int(ending_date[0])
                ending_date_month = int(ending_date[1])
                ending_date_day = int(ending_date[2])
                leave_to = date(ending_date_year,ending_date_month,ending_date_day)
                instance.leave_to = leave_to
            instance.approved = True
            instance.checked_on = datetime.today()
            instance.save()
            instance.user.employee.total_leave += 1
            instance.user.employee.save()
            # send mail that user's leave request rejected
            user_email = instance.user.email
            subject = "Your leave request is Approved"

            if request.POST['endingDate'] != "" and (leave_to - leave_from).days > 1:
                message = f"Dear {instance.user.first_name},\nYou have requested for leave and it's approved for {(leave_to - leave_from).days} days from {instance.leave_from} to {instance.leave_to}. You have to continue from {instance.leave_to+timedelta(days=1)}.\n\n{request.POST['message']}"
            else:
                message = f"Dear {instance.user.first_name},\nYou have requested for leave and it's approved for 1 day date is {instance.leave_from}. You have to continue from {instance.leave_from+timedelta(days=1)}.\n\n{request.POST['message']}"
            send_mail(user_email,subject,message)


def leave_requests(request):
    context ={'leave_requests_page':True}
    datetimenow = DateTimeNow.objects.create()
    
    if request.GET.get('view',None) == "all":
        leaveRequests = leaveApplication.objects.filter(approved = False,rejected=False).order_by('id')
        context['view_all'] = True
    else:
        leaveRequests = leaveApplication.objects.filter(date=datetimenow.date,approved = False,rejected=False).order_by('id')
        context['view_today'] = True

    context['leave_requests'] = leaveRequests

    # reject funtion 
    reject(request)

    # approve function 
    approve(request)

    return render(request,'secondery/leave_requests.html',context)