from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact 

def login(request):
    if request.method == 'POST':
        #Login
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else :
     return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
    return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)    


def register(request):
    if request.method == 'POST':
        #GET FORM VALUE
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #CHECK
        if password == password2:
            #Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email is being used')
                    return redirect('register')
                else:
                    #Looks Good
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    #Login
                    # auth.login(request, user)
                    # messages.success(request, 'You are logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'You are now registered and can login')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else :
      return render(request, 'accounts/register.html')