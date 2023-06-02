from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse

def auth_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        from app.view_function.auth_view import auth_function
        response = auth_function(request)
        return response

def Logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('auth')

@login_required(login_url='auth')
def index_view(request):
    from app.view_function.index_view import index
    response = index(request)
    return response


@login_required(login_url='auth')
def mark_attendance_view(request):
    from app.view_function.mark_attendance_view import mark_attendance
    response = mark_attendance(request)
    return response


def make_employee_sheet_view(request):
    from app.view_function.make_employee_sheet_view import make_employee_sheet
    response = make_employee_sheet(request)

    return response

def check_attendance_view(request):
    from app.view_function.check_attendance_view import check_attendance
    response = check_attendance(request)
    return response

def download_attendance_sheet_view(request):
    from app.view_function.download_attendance_sheet import download_attendance_sheet
    response = download_attendance_sheet(request)
    return response

def todays_attendance_view(request):
    from .view_function.todays_attendance_view import todays_attendance_view
    response = todays_attendance_view(request)
    return response

def download_todays_attendance_sheet(request):
    from .view_function.download_todays_attendance_sheet import download_todays_attendance_sheet
    response = download_todays_attendance_sheet(request)
    return response

def leave_requests_view(request):
    from .view_function.leave_requests_view import leave_requests
    response = leave_requests(request)
    return response