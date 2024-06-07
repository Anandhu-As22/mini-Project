from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import LoginForm,RegisterForm
from django.contrib import messages
# Create your views here.


# user login

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print('form is valid')
            name = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request,username=name,password=password)
            print(user)
            if user is not None:
                print('user')
                if user.is_active:
                    request.session['user']=name
                    login(request,user)
                    return redirect('home')
                else:
                    print('user blocked')
                    # messages.error(request,'user account is block')
            else:
                print('invalid')
                messages.error(request,"Invalid username or password")
                
    else:
        form = LoginForm()
    return render(request,'user-login.html',{'form':form,'messages':messages})




# user sign up

def user_signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect(user_login)
    else:
        form = RegisterForm()
    return render(request,'user-signup.html',{'form':form})





# user logout


def user_logout(request):
    
    logout(request)
    return redirect('index')



# admin login


def admin_login(request):
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            password = form.cleaned_data['password']
             
            user = authenticate(request,username=name,password=password)
            print(user)

            if user is not None:
                print('user')
                if user.is_staff:
                    print('super')
                    login(request,user)
                    request.session['adminn']=name
                    print(name)
                    return redirect('admin-home')
                else:
                    messages.error(request,'the user has no admin access')
            else:
                messages.error(request,'invalid username or password')
    else:
        form =LoginForm()
    return render(request,'admin_login.html',{'form':form})
  