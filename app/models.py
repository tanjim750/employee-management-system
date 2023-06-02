from django.db import models
from django.contrib.auth.models import User

class employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", null=True)
    number = models.CharField(max_length=14)
    position = models.CharField(max_length=25)
    department = models.CharField(max_length=25)
    dof = models.DateField()
    address = models.TextField()
    total_attd = models.IntegerField(default=0)
    total_leave = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.first_name)

class attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.DateField(auto_now_add=False)
    check_in = models.DateTimeField(auto_now_add=False)
    early_in = models.TimeField(null=True,blank=True)
    late_in = models.TimeField(null=True,blank=True)
    check_out = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    early_out = models.TimeField(null=True,blank=True)
    late_out = models.TimeField(null=True,blank=True)
    working_period = models.TimeField(null=True, blank=True)
    attend = models.BooleanField(default=False)
    leave = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user.first_name)

class DateTimeNow(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    dateTime = models.DateTimeField(auto_now_add=True)

class AttendanceTimeLimit(models.Model):
    JustInTime = models.TimeField()
    LateInTimeLimit = models.TimeField()
    JustOutTime = models.TimeField()

class holiday(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.name)
    
class leaveApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    application = models.TextField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    leave_from = models.DateField(null=True)
    leave_to = models.DateField(null=True)
    admin_message = models.TextField(null=True)
    checked_on = models.DateField(null=True)


