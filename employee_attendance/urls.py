"""employee_attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index_view, name='index'),
    path('auth',views.auth_view, name='auth'),
    path('mark-attendance', views.mark_attendance_view),
    path('logout', views.Logout, name="logout"),
    path('download-employee-sheet', views.make_employee_sheet_view, name="download-sheet"),
    path('check-attendance', views.check_attendance_view, name="check-attendance"),
    path('download-attendace-sheet', views.download_attendance_sheet_view),
    path('today-attendance', views.todays_attendance_view),
    path('download_todays_attendance_sheet',views.download_todays_attendance_sheet),
    path('leave-requests', views.leave_requests_view,name='leave-requests'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
