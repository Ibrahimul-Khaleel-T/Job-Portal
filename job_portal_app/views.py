from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import JobSeeker
from django.contrib.auth import authenticate,login,logout
from .models import User
from .models import Employee

# Create your views here
def index(request):
    return render(request,'index_page.html')

def jobseeker_signup(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        number=request.POST['number']
        password=request.POST['password']
        resume=request.FILES.get('resume')
        data=User.objects.create_user(username=username,password=password)
        data.save()
        details=JobSeeker.objects.create(user_id=data,firstname=firstname,lastname=lastname,email=email,number=number,resume=resume)
        details.save()
        return HttpResponse("success")
    else:
        return render(request,'seeker_signup.html')

def jobseeker_signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponse("success")
        else:
            return render(request,'seeker_signin.html',{'error':'Invalid username or password'})
    else:
        return render(request,'seeker_signin.html')

def employee_signup(request):
    if request.method=='POST':
        companyname=request.POST['companyname']
        email=request.POST['email']
        companyindustry=request.POST['companyindustry']
        discription=request.POST['discription']
        username=request.POST['username']
        password=request.POST['password']
        companylogo=request.FILES.get('companylogo')
        data=User.objects.create_user(username=username,password=password,user_type="employee")
        data.save()
        details=Employee.objects.create(user_id=data,companyname=companyname,companyindustry=companyindustry,discription=discription,companylogo=companylogo)
        details.save()
        return HttpResponse("success")
    else:
        return render(request,'employee_signup.html')

def employee_signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if user.user_type=='employee':
                
            return HttpResponse("success")
        else:
            return render(request,'employee_signin.html',{'error':'Invalid username or password'})
    else:
        return render(request,'employee_signin.html')