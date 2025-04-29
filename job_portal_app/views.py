from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import JobSeeker
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from .models import Employee
from django.core.mail import send_mail
import random
from django.contrib import messages
from .models import Job,Application,EmailRecord
from django.views.generic import DeleteView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings




# Create your views here
def index(request):
    return render(request,'index_page.html')


def seeker_home(request):
    current_date = timezone.now().date()
    jobs = Job.objects.filter(application_deadline__gte=current_date)
    return render(request, 'seeker_feed.html', {'jobs': jobs})


def job_ajax_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail_snippet.html', {'job': job})


def employee_home(request):
    employee=Employee.objects.get(user_id=request.user)
    jobs=Job.objects.filter(posted_by=employee)
    applications=Application.objects.filter(job__in=jobs).select_related('job','jobseeker')
    context={'applications':applications}
    return render(request,'employee_feed.html',context)


def load_applicant_details(request, id):
    application = get_object_or_404(Application, id=id)
    return render(request, 'applicant_detail_snippet.html', {'application': application})


def jobseeker_signup(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        number=request.POST['number']
        password=request.POST['password']
        resume=request.FILES.get('resume')
        dp=request.FILES.get('dp')
        data=CustomUser.objects.create_user(username=username,email=email,password=password,user_type="jobseeker")
        data.save()
        details=JobSeeker.objects.create(user_id=data,firstname=firstname,lastname=lastname,number=number,resume=resume,dp=dp)
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
                return HttpResponse("Unknown user")
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
        if 'dp' in request.FILES:
            jobseeker.dp=request.FILES['dp']
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
        data=Job.objects.create(posted_by=employee,user_id=request.user,job_title=job_title,discription=discription,requirements=requirements,salary_range=salary,location=location,application_deadline=deadline)
        data.save()
        return render(request,'job_posted_success.html')
    else:
        return render(request,'job_post.html')


def job_details(request,id):
    job=Job.objects.get(id=id)
    return render(request, 'job_details.html',{'job':job})


def select_edit_job_post(request):
    employee=Employee.objects.get(user_id=request.user)
    jobs=Job.objects.filter(posted_by=employee)
    return render(request,'select_edit_job_post.html',{'jobs':jobs})


def edit_job_post(request,id):
    job=Job.objects.get(id=id)
    if request.method=='POST':
        job.job_title=request.POST['job_title']
        job.discription=request.POST['discription']
        job.requirements=request.POST['requirements']
        job.salary_range=request.POST['salary']
        job.location=request.POST['location']
        job.application_deadline=request.POST['deadline']
        job.save()
        return redirect(select_edit_job_post)
    else:
        return render(request,'edit_job_post.html',{'job':job})


class JobDeleteView(DeleteView):
    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        job_title = job.job_title
        job.delete()
        messages.success(request, f"The job post of '{job.job_title}' was deleted successfully.")
        return redirect(select_edit_job_post)


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    jobseeker = get_object_or_404(JobSeeker, user_id=request.user)

    Application.objects.create(job=job, jobseeker=jobseeker)

    employer_email = job.posted_by.user_id.email

    subject = f"New Application for: {job.job_title}"
    message = f"{jobseeker.firstname} {jobseeker.lastname} has applied for {job.job_title}.\n\nCheck the resume attached."

    email = EmailMessage(subject, message, to=[employer_email])
    if jobseeker.resume:
        email.attach_file(jobseeker.resume.path)
    email.send()
    messages.success(request, f"Your application was sent to '{job.posted_by.companyname}'!")
    return redirect('seeker_home')


def job_application_response(request,application_id):
    application = get_object_or_404(Application, id=application_id)
    job=application.job
    jobseeker = application.jobseeker
    applicant_email = jobseeker.user_id.email

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
                subject="Congratulations! Interview Scheduled"
                message=f"Dear {jobseeker.firstname} {jobseeker.lastname},\n\nCongratulations! You have been shortlisted for the application of {job.posted_by.companyname} for {job.job_title}. We will contact you soon with the schedule.\n\nBest regards,\n{job.posted_by.companyname}"
                
                email = EmailMessage(subject,message,to=[applicant_email])
                email.send()
        elif action == 'reject':
                subject="Application Update"
                message=f"Dear {jobseeker.firstname} {jobseeker.lastname},\n\nThank you for your interest. After careful consideration, we regret to inform you that you have not been selected.\n\nBest wishes,\n{job.posted_by.companyname}"
                
                email=EmailMessage(subject,message,to=[applicant_email])
                email.send()
        EmailRecord.objects.create(jobseeker=jobseeker,job=job,action=action,subject=subject,message=message)
        messages.success(request,f"Your response was sent to '{jobseeker.firstname} {jobseeker.lastname}'!")
        return redirect(employee_home) 

    return render(request, 'employee_home.html')


def seeker_notification(request):
    jobseeker=JobSeeker.objects.get(user_id=request.user.pk)
    emails=EmailRecord.objects.filter(jobseeker=jobseeker).order_by('-sent_at')
    return render(request,'seeker_notification.html',{'emails':emails}) 


def seeker_notification_detail(request, id):
    notification = get_object_or_404(EmailRecord, id=id)
    return render(request, 'seeker_notification_snippet.html', {'notification': notification})





    


    


    
    







