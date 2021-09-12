from django import forms


class ContactForm(forms.Form):
    name=forms.CharField(label="Your name", max_length=100)