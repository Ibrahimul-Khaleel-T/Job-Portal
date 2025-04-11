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

class Employee(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    companyname=models.CharField(max_length=25)
    companyindustry=models.CharField(max_length=25)
    discription=models.CharField(max_length=250)
    companylogo=models.FileField(null=True,blank=True)
