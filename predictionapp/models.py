from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Adddoctor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.CharField(max_length=100, null=True, blank=True)
    fee = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.user.username


STATUS = ((1, "Read"), (2, "Unread"))
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

STATUS = ((1, "Approve"), (2, "Deny"))
class Blood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nam = models.CharField(max_length=100, null=True, blank=True)
    male = models.CharField(max_length=100, null=True, blank=True)
    bloodgroup=models.CharField(max_length=100, null=True, blank=True)
    mobilenumber = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# STATUS = ((1, "Approve"), (2, "Deny"))
# class Blood(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     bloodgroup=models.CharField(max_length=100, null=True, blank=True)
#     mobilenumber = models.IntegerField(max_length=100, null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     status = models.IntegerField(choices=STATUS, default=2)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user.username

class diseaseinfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    diseasename = models.CharField(max_length = 200)
    no_of_symp = models.IntegerField(null=True, blank=True,default=0)

    symptomsname = ArrayField(models.CharField(max_length=200),default=list)
    confidence = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
         return self.user.username













