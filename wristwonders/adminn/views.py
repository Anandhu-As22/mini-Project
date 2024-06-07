from django.shortcuts import render,redirect
from authentication.views import admin_login
from Customers.models import User
from authentication.forms import RegisterForm
from .forms import UpdateForm
# Create your views here.


def admin_home(request):
    if request.user.is_authenticated:
        return render(request,'admin_home.html')
    return redirect(admin_login)


def User_list(request):
   if 'adminn' in request.session:
       user = User.objects.all()
       return render(request,'users.html',{'user':user})
   return redirect(admin_login)


def add_user(request):
    if 'adminn' in request.session:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                print(user)
                return redirect('adminn-user-list')
        else:
            form = RegisterForm()
        return render(request,'add-user.html',{'form':form})
    return redirect(admin_login)

def Update_user(request,pk):
    if 'adminn' in request.session:
        instance = User.objects.get(id=pk)
        form = UpdateForm(instance=instance)
        if request.POST:
            fm = UpdateForm(request.POST,instance=instance)
            if fm.is_valid:
                fm.save()
                return redirect('adminn-user-list')
            else:
                form=UpdateForm(instance=instance)
        return render(request,'update-user.html',{'form':form})
    return redirect(admin_login)

# block user
def block_user(request,pk):
    if 'adminn' in request.session:
        instance = User.objects.get(id =pk)
        instance.is_active = False
        instance.save()
        return redirect('adminn-user-list')
    return redirect(admin_login)


# unblock user
def Un_block_user(request,pk):
    if 'adminn' in request.session:
        instance = User.objects.get(id =pk)
        instance.is_active = True
        instance.save()
        return redirect('adminn-user-list')
    return redirect(admin_login)


