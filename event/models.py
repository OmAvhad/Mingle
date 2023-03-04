from django.db import models
from UserAccounts.models import *
# Create your models here.
class Events(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    event_name = models.CharField(max_length=200,null=True,blank=True)
    registeration_limit = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=False,null=True,blank=True)

class Rate(models.Model):
    stars = models.IntegerField(null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)


class OrganizationDetail(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    organization_address = models.TextField(null=True,blank=True)
    organization_logo = models.FileField(upload_to='logo')
    
class Image(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    file = models.FileField(upload_to='img')


class Icebreakers(models.Model):
    value = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=False)


class UserAppliedforEvents(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    event = models.ForeignKey(Events,on_delete=models.CASCADE,null=True,blank=True)
    applied_at = models.DateTimeField(auto_now=True,null=True,blank=True)


class Interest(models.Model):
    value = models.CharField(max_length=100,null=True,blank=True)