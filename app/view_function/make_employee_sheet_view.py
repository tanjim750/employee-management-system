import csv
from django.http import HttpResponse
from app.models import employee
from django.contrib.auth.models import User
import time
def make_employee_sheet(request):
    # Query all employees from the database
    employees = User.objects.all().exclude(is_superuser=True)

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee.csv"'

    # Create the CSV writer and write the header
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Number', 'Position', 'Department', 'Date of Birth', 'Address', 'Total Attendance', 'Total Leave'])

    # Write the employee data to the CSV
    for emp in employees:
        writer.writerow([emp.first_name, emp.last_name, emp.email, emp.employee.number, emp.employee.position, emp.employee.department, emp.employee.dof, emp.employee.address, emp.employee.total_attd, emp.employee.total_leave])

    # Set a cookie to indicate successful download
    response.set_cookie('downloaded', 'true', max_age=5)

    time.sleep(3)
    return response


