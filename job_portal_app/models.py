from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    user_type=models.CharField(max_length=25)


class JobSeeker(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=25)
    lastname=models.CharField(max_length=25)
    number=models.IntegerField(null=True,blank=True)
    resume=models.FileField(null=True,blank=True)
    dp=models.FileField(null=True,blank=True)


class Employee(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    companyname=models.CharField(max_length=25)
    companyindustry=models.CharField(max_length=25)
    discription=models.CharField(max_length=250)
    companylogo=models.FileField(null=True,blank=True)


class Job(models.Model):
    job_title=models.CharField(max_length=250)
    discription=models.TextField()
    requirements=models.TextField()
    salary_range=models.CharField(max_length=150)
    location=models.CharField(max_length=250)
    application_deadline=models.DateField()
    posted_by=models.ForeignKey(Employee,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)


class EmailRecord(models.Model):
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    action = models.CharField(max_length=10) 
    sent_at = models.DateTimeField(auto_now_add=True)

    
