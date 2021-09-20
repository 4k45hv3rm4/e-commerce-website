from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from django.contrib.auth.forms import UsernameField
from . import models


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ('email',)
        field_classes = {'email': UsernameField}
    
class ContactForm(forms.Form):
    name=forms.CharField(label="Your name", max_length=100)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

