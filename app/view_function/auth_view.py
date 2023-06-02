from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect , render

def auth_function(request):
    context = {}
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']

        user = authenticate(request, username=id, password=password)

        if user is not None:
            login(request, user)

            return redirect('index')

        else:
            context['error'] = 'Employee id or Password incorrect'

    return render(request, 'secondery/auth.html', context)
        



        
