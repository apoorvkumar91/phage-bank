from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData, PeopleData, HostData


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', 'password1', 'password2',)

class AddPhageForm(forms.ModelForm):
    phage_first_name = forms.CharField(label='Phage First Name', max_length=30, required=True, help_text='Required.')
    phage_second_name = forms.CharField(label='Phage Second Name', max_length=30, required=True, help_text='Required.')

    class Meta:
        model = PhageData
        fields = ('phage_first_name', 'phage_second_name')

class AddPeopleForm(forms.ModelForm):
    people_first_name = forms.CharField(label='People First Name', max_length=30, required=True, help_text='Required.')
    people_second_name = forms.CharField(label='People Second Name', max_length=30, required=True, help_text='Required.')

    class Meta:
        model = PeopleData
        fields = ('people_first_name', 'people_second_name')

