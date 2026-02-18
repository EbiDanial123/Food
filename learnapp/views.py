from django.shortcuts import render, redirect
from learnapp.forms import UserForm,UserProfileForm,UserUpdateform,UserProfileUpdateform
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from learnapp.models import UserDetails
from foods.models import FoodItems        
from django.contrib import messages
               
# Create your views here.

def index(request):
    registered = False
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            profile = form2.save(commit=False)
            profile.user = user    #connecting two models to save the final data
            profile.save()
            registered = True
    else:
        form1 = UserForm()
        form2 = UserProfileForm()
    context = {
        'form1':form1,
        'form2':form2,
        'registered' : registered
    }
    return render(request,'index.html',context)

def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Allfoods')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')
@login_required(login_url='login')

def home(request):
    foods=FoodItems.objects.all()
    return render(request,'home.html',{'foods':foods})

@login_required(login_url="login")

def user_logout(request):
    logout(request)
    return redirect("login")
@login_required(login_url="login")
def profile(request):
        user_details, created = UserDetails.objects.get_or_create(user=request.user)
        return render(request, 'profile.html', {'user_details': user_details})


@login_required(login_url="login")
def userupdate(request):
    if request.method =='POST':
        form=UserUpdateform(request.POST,instance=request.user)
        form1=UserProfileUpdateform(request.POST,request.FILES,instance=request.user.userdetails)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()
            
            profile=form1.save(commit=False)
            profile.user = user
            profile.save()
            return redirect("profile")
    else:
        form=UserUpdateform(instance=request.user)
        form1=UserProfileUpdateform(instance=request.user.userdetails)
    context={
        'form':form,
        'form1':form1
    }
    return render(request,'update.html',context)