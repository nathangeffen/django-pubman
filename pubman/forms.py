'''This module contains the following forms:

UserProfile: form consisting of user editable fields 
    from pubman.models.UserProfile and 
    django.contrib.auth.models.User 

'''

from django import forms
from django.contrib.auth.models import User
from contact_form.forms import ContactForm 
from django.utils.translation import ugettext as _

from models import UserProfile
from stopspam.forms import HoneyPotForm
from stopspam.forms.fields import HoneypotField

class UserForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    class Meta(object):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


from sorl.thumbnail.admin import AdminClearableImageWidget
from sorl.thumbnail.fields import ClearableImageFormField

class UserProfileForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'    
    avatar = ClearableImageFormField(widget= AdminClearableImageWidget, required=False)
        
    def clean_avatar(self):

        data = self.cleaned_data['avatar']
        
        if data == False:
            return ""
        else:
            return data
    
    def save(self, commit=True, force_insert=False, force_update=False):
        self.instance.user = User.objects.get(pk=self.fields.user)        
        super(forms.ModelForm, self).save(commit=False)
        self.instance.save()
        
    class Meta(object):
        model = UserProfile
        exclude = ['user']
        widgets = {
               'date_of_birth': forms.TextInput(attrs={'class': 'datepicker'}),
        }

        
class PubmanContactForm(ContactForm):
    error_css_class = 'error'
    required_css_class = 'required'
    # This field will not be displayed to web users.
    # Hopefully spam bots will fill it in.
    accept_terms = HoneypotField() 
                                    
    subject = forms.CharField(max_length=100,
                           label=_('Subject'))
    
    def __init__(self, *args, **kwargs):
        ContactForm.__init__(self, *args, **kwargs)
        self.fields.keyOrder = ['name', 'email', 'subject', 'accept_terms', 'body']

