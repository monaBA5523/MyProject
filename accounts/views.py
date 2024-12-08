from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'],email=data['email'],first_name=data['first_name'],
                                   last_name=data['last_name'] ,password=data['password_2'])
            user.save()
            messages.success(request,'ثبت نام شما با موفقیت انجام شد','success')
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    return render(request,'accounts/register.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
           data = form.cleaned_data
           try:
              user = authenticate(request,username=User.objects.get(email=data['email'],password=data['password']))
           except :
              user = authenticate(request,username=data['user'],password=data['password'])
           if user is not None:
                login(request,user)
                messages.success(request, 'خوش آمدید', 'info')
                return redirect('home:home')
           else:
               messages.error(request,'نام کاربری درست وارد نشده است','danger')
    else:
         form = UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})


def user_logout(request):
    logout(request)
    messages.success(request,'به امید دیدار','warning')
    return redirect('home:home')

def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request,'accounts/profile.html',{'profile':profile})


def user_update(request):
   if request.method == 'POST':
       user_form = UserUpdateForm(request.POST,instance=request.user)
       profile_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
       if user_form and profile_form.is_valid():
           user_form.save()
           profile_form.save()
           return redirect('accounts:profile')
   else:
       user_form = UserUpdateForm(instance=request.user)
       profile_form = ProfileUpdateForm(instance=request.user.profile)
   return render(request,'accounts/update.html',{'user_form':user_form,'profile_form':profile_form})
