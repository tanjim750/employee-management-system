from django.shortcuts import redirect, render
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

#For Send html template to email
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils.timezone import now

def index(request):
    # return dictionary
    context = {'index_page':True}
    dateTimeNow = DateTimeNow.objects.create()

    # application form 
    application = """
Date: 01/01/2023
To,
{name}
{position}
From,
{name}
{position}
Subject: Leave Application

Dear Mr./Mrs. {Recipient’s Name},

I am writing to request you for a leave of {X days} from {start date} to {end date} since I have to attend to a medical emergency of a close relative. As the relative is situated in Uttrakhand, I will have to be away for {X days}. I will resume work from {mention date}.

I shall be reachable on my mobile number and email during the period. My person in charge, {person's name} will be handling my tasks in my absence.

I will be thankful to you for considering my application.

Yours Sincerely,
{Your Name}
    """
    application_exists = leaveApplication.objects.filter(Q(user=request.user) & Q(date=dateTimeNow.date) | Q(checked_on = dateTimeNow.date))
    context['application_exists'] = application_exists
    context['application'] = application

    _AttendanceTimeLimit = AttendanceTimeLimit.objects.get(id=1)
    context["DateTimeNow"] = dateTimeNow
    context["lateInTimeLimit"] = _AttendanceTimeLimit.LateInTimeLimit
    
    if request.user.is_superuser :
        Employees = User.objects.all().exclude(is_superuser = True).order_by("-id")
        context['employees'] = Employees
    else:
        Employees = User.objects.get(username=request.user.username)
        Attendance = attendance.objects.filter(user=request.user,day=dateTimeNow.date).first()
        if Attendance is not None:
            context["working_time"] = dateTimeNow.dateTime - Attendance.check_in
            context["minimum_time"] = timedelta(minutes=30)
        context['employe'] = Employees
        context['checkedIn'] = Attendance
    
    make_actions = request.GET.get('action', None)

    if make_actions is not None:
        if make_actions == "add-employee":
            return render(request, 'secondery/add.html', context)
        elif make_actions == "delete":
            username = request.GET.get('id',None)
            if username is not None:
                User.objects.get(username=username).delete()
            return redirect("index")
        
        elif make_actions == "edit":
            username = request.GET.get('id',None)
            if username is not None:
                get_employee = User.objects.get(username=username)
                context["employee"] = get_employee
            return render(request, 'secondery/add.html', context)
    
    # manage employee
    if request.method == "POST":
        # add new employee
        if request.POST["action"] == "addnew":
            image = request.FILES["image"]
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            emailaddr = request.POST["email"]
            number = request.POST["number"]
            position = request.POST["position"]
            department = request.POST["department"]
            dof = request.POST["dof"]
            address = request.POST["address"]

            import secrets
            import string

            # Define the alphabet
            alphabet = string.ascii_letters + string.digits

            digits = string.digits

            #password length
            password_length = 8

            username_length = 9

            # Generate the password
            password = ""
            for _ in range(password_length):
                password += secrets.choice(alphabet)
        
            def make_username(length):
                username = ""
            
                for _ in range(username_length):
                    username += secrets.choice(digits)

                return username
            
            loop = True
            while loop:
                username = make_username(username_length)
                username_exists = User.objects.filter(username=username).exists()

                if not username_exists:
                    loop = False

            user = User.objects.create(
                username = username,
                password = make_password(password),
                first_name = fname,
                last_name = lname,
                email = emailaddr,
            )

            employee.objects.create(
                user = user,
                position =position,
                department = department,
                dof = dof,
                number = number,
                address = address,
                image = image
            )


            # send user login credentials to employee email

            subject = 'Your login credentials'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            html_template = render_to_string('email_template/welcome.html',{'username':user.username, 'email':user.email, 'title':subject, 'password':password, 'fname':user.first_name,'lname':user.last_name})
            message = strip_tags(html_template)
            email = EmailMultiAlternatives(
                    subject,
                    message,
                    email_from,
                    recipient_list
            )
            email.attach_alternative(html_template, 'text/html')
            email.send()
            context['success'] = True
            context['success_msg'] = "The new Employee added successfully."
            

        # edit employee details
        elif request.POST["action"] == "edit":

            
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            emailaddr = request.POST["email"]
            number = request.POST["number"]
            position = request.POST["position"]
            department = request.POST["department"]
            dof = request.POST["dof"]
            address = request.POST["address"]
            username = request.POST["id"]

            user = User.objects.get(username=username)

            try:
                image = request.FILES["image"]

                user.employee.image = image
                user.employee.save()
            except:
                pass

            user.first_name = fname
            user.last_name = lname
            user.email = emailaddr
            user.employee.number = number
            user.employee.position = position
            user.employee.department = department
            user.employee.dof = dof
            user.employee.address = address
            user.save()
            user.employee.save()
            context['success'] = True
            context['success_msg'] = "Employee Information has been successfully edited"

        # make leave request 
        elif request.POST['action'] == "leave_request":
            application_text = request.POST['application']
            user = request.user
            leaveApplication.objects.create(
                user = user,
                application = application_text
            )

            # send mail that user made a leave request

            subject = f'{user.first_name} {user.last_name} requested for leave'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            html_template = render_to_string('email_template/leave_request.html',{'user':user, 'title':subject, 'fname':user.first_name,'lname':user.last_name,'application':application_text})
            message = strip_tags(html_template)
            email = EmailMultiAlternatives(
                    subject,
                    message,
                    email_from,
                    recipient_list
            )
            email.attach_alternative(html_template, 'text/html')
            email.send()

    
    return render(request, 'secondery/index.html', context)