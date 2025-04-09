from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobSeeker(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=25)
    lastname=models.CharField(max_length=25)
    email=models.CharField(max_length=35)
    number=models.IntegerField(null=True,blank=True)
    resume=models.FileField(null=True,blank=True)

class Employee(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    companyname=models.CharField(max_length=25)
    companyindustry=models.CharField(max_length=25)
    discription=models.CharField(max_length=250)
    website=models.CharField(max_length=25)
    companylogo=models.FileField(null=True,blank=True)
