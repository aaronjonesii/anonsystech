# https://docs.djangoproject.com/en/2.1/ref/forms/fields/
from django import forms


class ContactForm(forms.Form):
    sender = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    cc_myself = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control'}))

    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
        
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}))

