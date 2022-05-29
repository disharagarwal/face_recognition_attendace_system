#this file is used to access and create the data, it maps to the data base table
from time import time
from django.db import models

#The Profile model is used to store the data of a profile with all the given fields
types = [('employee','employee'),('visitor','visitor')]
class Profile(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    date = models.DateField()
    phone = models.BigIntegerField()
    email = models.EmailField()
    profession = models.CharField(max_length=200)
    status = models.CharField(choices=types,max_length=20,null=True,blank=False,default='employee')
    present = models.BooleanField(default=False)
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)
    updated_date=models.DateField(auto_now=True)
    shift = models.TimeField()
    def __str__(self):
        return self.first_name +' '+self.last_name

class LastFace(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    date_date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.last_face

class ExcelFileUpload(models.Model):
    excel_file_upload=models.FileField(upload_to="excel")