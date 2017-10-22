from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', 'password1', 'password2',)

class AddPhageForm(forms.ModelForm):
    phage_name = forms.CharField(label='Phage Name', max_length=30, required=True, help_text='Required.')
    host_name = forms.CharField(label='Host Name', max_length=30, required=True, help_text='Required.')

    class Meta:
        model = PhageData
        fields = ('phage_name', 'host_name')