from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import JobSeeker
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from .models import Employee
from django.core.mail import send_mail
import random
from django.contrib import messages
from .models import Job
from django.utils import timezone

# Create your views here
def index(request):
    return render(request,'index_page.html')

def seeker_home(request):
    jobs=Job.objects.all()
    return render(request,'seeker_feed.html',{'jobs':jobs})

def employee_home(request):
    return render(request,'employee_feed.html')

def jobseeker_signup(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        number=request.POST['number']
        password=request.POST['password']
        resume=request.FILES.get('resume')
        data=CustomUser.objects.create_user(username=username,email=email,password=password,user_type="jobseeker")
        data.save()
        details=JobSeeker.objects.create(user_id=data,firstname=firstname,lastname=lastname,number=number,resume=resume)
        details.save()
        user=authenticate(username=username,password=password)
        login(request,user)
        return redirect(seeker_home)
    else:
        return render(request,'seeker_signup.html')

def employee_signup(request):
    if request.method=='POST':
        companyname=request.POST['companyname']
        email=request.POST['email']
        companyindustry=request.POST['companyindustry']
        discription=request.POST['discription']
        username=request.POST['username']
        password=request.POST['password']
        companylogo=request.FILES.get('companylogo')
        data=CustomUser.objects.create_user(email=email,username=username,password=password,user_type="employee")
        data.save()
        details=Employee.objects.create(user_id=data,companyname=companyname,companyindustry=companyindustry,discription=discription,companylogo=companylogo)
        details.save()
        user=authenticate(username=username,password=password)
        login(request,user)
        return redirect(employee_home)
    else:
        return render(request,'employee_signup.html')
    

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if user.user_type=='employee':
                return redirect(employee_home)
            elif user.user_type=='jobseeker':
                return redirect(seeker_home)
            else:
                return HttpResponse("Error")
        else:
            return render(request,'signin.html',{'error':'Invalid username or password'})
    else:
        return render(request,'signin.html')
    
def Logout(request):
    logout(request)
    return redirect(signin)

    
def send_otp(email):
    otp = random.randint(100000,999999)
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'kha7ee7@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        try:
            user = CustomUser.objects.get(email=email)
            otp = send_otp(email)
            print(otp)

            context = {
                        "email": email,
                        "otp": otp,
            }
            return render(request,'verify_otp.html',context)
        
        except CustomUser.DoesNotExist:
            messages.error(request,'Email address not found.')
    else:
        return render(request,'reset_password.html')
    return render(request,'reset_password.html') 

def verify_otp(request):
    if request.method == 'POST':
        email =request.POST.get('email')
        otpold = request.POST.get('otpold')
        otp = request.POST.get('otp')

        if otpold==otp :
            context = {
                'otp' : otp,
                'email': email
            }
            return render(request,'set_new_password.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'verify_otp.html') 

def set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password==confirm_password:
            try:
                data = CustomUser.objects.get(email=email)
                data.set_password(new_password)
                data.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(signin)
            except CustomUser.DoesNotExist:
                messages.error(request,'Password doesnot match')
        return render(request,'set_new_password.html',{'email':email})               
    return render(request,'set_new_password.html',{'email':email})


def seeker_profile(request):
    try:
        jobseeker = JobSeeker.objects.get(user_id=request.user)
        custom_user = request.user

        return render(request, 'seeker_profile.html', {
            'data': jobseeker,
            'details': custom_user
        })
    except JobSeeker.DoesNotExist:
        return redirect('seeker_home')

    except:
        return redirect(seeker_home)
    
def employee_profile(request):
    try:
        employee=Employee.objects.get(user_id=request.user)
        custom_user=request.user

        return render(request,'employee_profile.html',{'data':employee,'details':custom_user})
    except Employee.DoesNotExist:
        return redirect('employee_home')   
    except:
        return redirect(employee_home)

   
def seeker_edit(request):
    jobseeker=JobSeeker.objects.get(user_id=request.user)
    custom_user=request.user
    if request.method=='POST':
        jobseeker.firstname=request.POST['firstname']
        jobseeker.lastname=request.POST['lastname']
        custom_user.username=request.POST['username']
        custom_user.email=request.POST['email']
        jobseeker.number=request.POST['number']
        if 'resume' in request.FILES:
            jobseeker.resume = request.FILES['resume']

        jobseeker.save()
        custom_user.save()

        return render(request, 'seeker_profile.html', {'data': jobseeker, 'details': custom_user})
    
    else:
        return render(request,'seeker_edit.html',{'data':jobseeker,'details':custom_user})
    
def employee_edit(request):
    employee=Employee.objects.get(user_id=request.user)
    custom_user=request.user
    if request.method=='POST':
        if 'companylogo' in request.FILES:
            employee.companylogo=request.FILES['companylogo']
        employee.companyname=request.POST['companyname']
        custom_user.email=request.POST['email']
        employee.companyindustry=request.POST['companyindustry']
        employee.discription=request.POST['discription']
        custom_user.username=request.POST['username']

        employee.save()
        custom_user.save()

        return render(request, 'employee_profile.html',{'data':employee,'details':custom_user})
    
    else:
        return render(request,'employee_edit.html',{'data':employee,'details':custom_user})
    
def job_post(request):
    if request.method=='POST':
        job_title=request.POST['job_title']
        discription=request.POST['discription']
        requirements=request.POST['requirements']
        salary=request.POST['salary']
        location=request.POST['location']
        deadline=request.POST['deadline']
        employee=Employee.objects.get(user_id=request.user)
        data=Job.objects.create(posted_by=employee,job_title=job_title,discription=discription,requirements=requirements,salary_range=salary,location=location,application_deadline=deadline)
        data.save()
        return HttpResponse("job posted successfully...")
    else:
        return render(request,'job_post.html')
    
def select_edit_job_post(request):
    if request.method=='POST':
        return render(request,'edit_job_post.html')
    else:
        employee=Employee.objects.get(user_id=request.user)
        jobs=Job.objects.filter(posted_by=employee)
        return render(request,'select_edit_job_post.html',{'jobs':jobs})
    
    
def job_details(request,id):
    job=Job.objects.get(id=id)
    return render(request, 'job_details.html',{'job':job})






