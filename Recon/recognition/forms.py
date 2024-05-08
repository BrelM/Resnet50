from django import forms
from .models import *

class DateInput(forms.DateInput):
    '''
    '''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }
      
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)  
        self.fields['image'].widget.attrs['class'] = 'form-control'
        