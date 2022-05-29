#admin.py is default file while creating a project in Django
#It is used to display your models in Django

from django.contrib import admin #automatic admin interface
from .models import *

admin.site.register(Profile) #registering the models from model.py 
admin.site.register(LastFace)#registering the models from model.py 