from django import forms #django has some range of forms(HTML) to accept inputs
from .models import *

#django's form class
class DateInput(forms.DateInput):#input of date 
    input_type = 'date'
class TimeInput(forms.TimeInput): #input of time
    input_type = 'time'

#class for filling the persons detalils in Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'date': DateInput(),
            'shift':TimeInput()
        }
        exclude = ['present','updated']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        #self.fields['ranking'].widget.attrs['class'] = 'form-control'
        self.fields['profession'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        #self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['shift'].widget.attrs['class'] = 'form-control'