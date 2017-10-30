from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from django.core.urlresolvers import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Accordion, AccordionGroup
from crispy_forms.layout import Submit, Layout, Div, Fieldset

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', 'password1', 'password2',)

class AddPhageForm(forms.ModelForm):
    phage_name = forms.CharField(label='Phage Name',
                                 max_length=30, required=True,
                                 help_text='Required.')

    phage_host_name = forms.CharField(label='Host Name',
                                      max_length=30, required=True,
                                      help_text='Required.')

    phage_isolator_name = forms.CharField(label='Isolator Name',
                                          max_length=30,
                                          required=True,
                                          help_text='Required.')

    phage_experimenter_name = forms.CharField(label='Experimenter Name',
                                              max_length=30,
                                              required=True,
                                              help_text='Required.')

    phage_CPT_id = forms.CharField(label='CPT id',
                                   max_length=30,
                                   required=True,
                                   help_text='Required.')

    phage_isolator_loc = forms.CharField(label='Isolator Location',
                                         max_length=5000,
                                         required=True,
                                         help_text='Required.')

    class Meta:
        model = PhageData
        fields = ('phage_name', 'phage_host_name',
                  'phage_isolator_name', 'phage_experimenter_name',
                  'phage_CPT_id', 'phage_isolator_loc')


    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'accordion'
    helper.field_class = 'accordion'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
    helper.layout = Layout(
        HTML("<button class='accordion'>Phage Data</button>"),
        HTML("<div class='panel'>"),
        Div('phage_name', 'phage_host_name', 'phage_CPT_id'),
        HTML("</div>"),
        HTML("<button class='accordion'>Researcher Details</button>"),
        HTML("<div class='panel'>"),
        Div('phage_isolator_name', 'phage_experimenter_name'),
        HTML("</div>"),
        HTML("<button class='accordion'>Research Information</button>"),
        HTML("<div class='panel'>"),
        Div('phage_isolator_loc'),
        HTML("</div>"),
        HTML("<br><br>")
    )




