from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate,get_user_model
from .forms import LoginForm,RegisterForm
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse
from django .template.loader import render_to_string
from Customers.models import User,Wallet,Wishlist
import time
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
            user = form.save(commit=False)
            user.is_active = False
            print(user)

            # generate otp
            otp = get_random_string(length=6,allowed_chars='0123456789')
            

           
           
            print(otp)

            # send otp via email

            subject = 'account verification'
            try:

                message = render_to_string('otp_verification_email.html',{'otp':otp,'username':user.username})
            except Exception as e:
                print(e)
                print('message error')

            from_email = 'asanandhu2001@gmail.com'
            recipient_list = [user.email]

            # if not isinstance(from_email, str):
            #     print(f"from_email is not a string: {from_email}")

            # if not all(isinstance(recipient, str) for recipient in recipient_list):
            #     print(f"Recipient list contains non-string: {recipient_list}")


            # if not isinstance(subject, str):
            #     print(f"Subject is not a string: {subject}")
            #     print('invalid email subject')
                
            # if not isinstance(message, str):
            #     print(f"Message is not a string: {message}")
            #     print('INVALID MESSAGE')
            # if not all(isinstance(recipient, str) for recipient in recipient_list):
            #     print(f"Recipient list contains non-string: {recipient_list}")
            #     print('invalid receipient email')
            try:
                # print(f"Sending email from: {from_email}")
                # print(f"Sending email to: {recipient_list}")
                # print(f"Subject: {subject}")
                # print(f"Message: {message}")
                send_mail(subject, message, from_email, recipient_list)
                request.session['otp']=otp
                request.session['username']=user.username
                request.session['otp_send_time'] = time.time()
                request.session['password'] = user.password
                request.session['email']=user.email
                request.session['first_name'] =user.first_name
                request.session['last_name'] = user.last_name
            
                # user.save()
                return redirect(otp_verification)
            except Exception as e:
                print(e)
                print('error in sending')
                
            
        else:
            print('fform is invalid')
            form = RegisterForm(request.POST)


            
    else:
        form = RegisterForm()
    return render(request,'user-signup.html',{'form':form})



# otp verification

def otp_verification(request):
    
    
    if request.method == "POST":
        username= request.session.get('username')
        otp = request.session.get('otp')
        otp_send_time = request.session.get('otp_send_time')
        time_now = time.time()
        password = request.session.get('password')
        email = request.session.get('email')
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
    
            
        entered_otp = request.POST.get('otp')
        if  time_now-otp_send_time<30:


            if entered_otp == otp:
            
                user = User.objects.create(email = email,username = username,first_name=first_name,last_name=last_name,password=password)
                Wallet.objects.create(user=user)
                Wishlist.objects.create(user=user)

                del request.session['otp']
                del request.session['username']
                del request.session['email']
                del request.session['first_name']
                del request.session['password']
                del request.session['last_name']
                del request.session['otp_send_time']

                return redirect(user_login)  # Redirect to login page
        
            else:
                messages.error(request,'Invalid otp,please try again')
                return render(request,'otp_verification .html', {'username': username})
        else:
            messages.error(request,'otp expired')
            return render(request,'otp_verification .html',{'username':username})
    
            
    return render(request,'otp_verification .html')


# resend otp 

def resend_otp(request):
    otp_send_time = request.session.get('otp_send_time')
    username = request.session.get('username')
    email = request.session.get('email')
    if time.time() - otp_send_time > 30:
        otp = get_random_string(length=6,allowed_chars='0123456789')
           
        print(otp)

            # send otp via email

        subject = 'account verification'
        try:

            message = render_to_string('otp_verification_email.html',{'otp':otp,'username':username})
        except Exception as e:
            print(e)
            print('message error')

        from_email = 'asanandhu2001@gmail.com'
        recipient_list = [email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            request.session['otp']=otp
            request.session['otp_send_time'] = time.time()
            return redirect(otp_verification)
        except Exception as e:
            print(e)
    return redirect(otp_verification)
        

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        user = User.objects.filter(email = email).first()
        print(user)

        if user:
            username = user.username
            print(username)
            otp = get_random_string(length=6,allowed_chars='0123456789')
            subject = 'password reset'

            try:
                message = render_to_string('forgotpasswordcontent.html',{'otp':otp,'username':username})
            
            except Exception as e:
                print(e)
            from_email = 'asanandhu2001@gmail.com'
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                request.session['otpp'] = otp
                request.session['emaill']=email
                return redirect(forgot_password_otp_verification)
                
            except Exception as e:
                print(e,'2nd')
        else:
            messages.error(request, "The email address you entered is not registered.")

    return render(request,'forgotpassword.html')
        



def forgot_password_otp_verification(request):
    if request.method == "POST":
        given_otp = request.POST.get('otp')
        otp = request.session.get('otpp')

        if given_otp == otp:
            print('entered forgot password')
            del request.session['otpp']
            return redirect(forgot_password_verification)
        else:
            messages.error(request,"the otp is incorrect")
    return render(request,'otp_verification .html')
    

def forgot_password_verification(request):
    if request.method == "POST":
        email = request.session.get('emaill')
        if email is None:
            messages.error(request, "Session expired. Please try the password reset process again.")
            return redirect(forgot_password)
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            messages.error(request, "User not found. Please try the password reset process again.")
            return redirect(forgot_password)
       
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 8:
            error_message = "Password must be at least 8 characters long"
            return render(request,'password-change.html', {'error_message': error_message})

        if password1 == password2:
            user.set_password(password1)
            user.save()
            del request.session['emaill']
            return redirect(user_login)
        else:
            messages.error(request,'two passwords must be same')
    return render(request,'password-change.html')


    



    





# user logout

@never_cache
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
  
@never_cache
def adminn_logout(request):
    
    logout(request)
    return redirect(admin_login)


