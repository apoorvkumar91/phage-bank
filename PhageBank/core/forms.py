from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Accordion, AccordionGroup
from crispy_forms.layout import Submit, Layout, Div, Fieldset, MultiField
from crispy_forms.layout import Submit, Reset, HTML
from crispy_forms.layout import Button
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet


def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(u'File In  CSV format Only')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(validators=[validate_file_extension])

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', 'password1', 'password2',)


class LoginForm(forms.ModelForm):

    username = forms.CharField(max_length=30, required=False)
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ("username", "password",)

class Add_Phage_DataForm(forms.ModelForm):
    phage_name = forms.CharField(label='Phage Name',
                                 max_length=30,
                                 required=True,
                                 help_text='Required.',
                                 widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                               'autocomplete': 'off',
                                                               'size': '100',
                                                               'style': 'font-size: small',
                                                               })
                                 )

    phage_host_name = forms.CharField(label='Host Name',
                                      max_length=30,
                                      required=False,
                                      help_text='Required.',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )

    class Meta:
        model = PhageData
        fields = ("phage_name", "phage_host_name",)

class Add_ResearcherForm(forms.ModelForm):
    phage_isolator_name = forms.CharField(label='Isolator Name',
                                          max_length=30,
                                          required=False,
                                          help_text='Required.',
                                          widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                        'autocomplete': 'off',
                                                                        'size': '100',
                                                                        'style': 'font-size: small',
                                                                        })
                                          )

    phage_experimenter_name = forms.CharField(label='Experimenter Name',
                                              max_length=30,
                                              required=False,
                                              help_text='Required.',
                                              widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                            'autocomplete': 'off',
                                                                            'size': '100',
                                                                            'style': 'font-size: small',
                                                                            })
                                              )

    class Meta:
        model = PhageData
        fields = ("phage_isolator_name", "phage_experimenter_name",)

class Add_ResearchForm(forms.ModelForm):
    phage_CPT_id = forms.CharField(label='CPT id',
                                   max_length=30,
                                   required=False,
                                   help_text='Optional.',
                                   widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                 'autocomplete': 'off',
                                                                 'size': '100',
                                                                 'style': 'font-size: small',
                                                                 })
                                   )

    phage_isolator_loc = forms.CharField(label='Isolator Location',
                                         max_length=5000,
                                         required=False,
                                         help_text='Required.',
                                         widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                       'autocomplete': 'off',
                                                                       'size': '100',
                                                                       'style': 'font-size: small',
                                                                       })
                                         )

    class Meta:
        model = PhageData
        fields = ("phage_CPT_id", "phage_isolator_loc",)


class AddPhageForm(forms.ModelForm):
    phage_name = forms.CharField(label='Phage Name',
                                 max_length=30,
                                 required=True,
                                 help_text='Required.',
                                 widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                               'autocomplete': 'off',
                                                               'size': '100',
                                                               'style': 'font-size: small',
                                                               })
                                 )

    phage_host_name = forms.CharField(label='Host Name',
                                      max_length=30,
                                      required=True,
                                      help_text='Required.',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )

    phage_isolator_name = forms.CharField(label='Isolator Name',
                                          max_length=30,
                                          required=True,
                                          help_text='Required.',
                                          widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                        'autocomplete': 'off',
                                                                        'size': '100',
                                                                        'style': 'font-size: small',
                                                                        })
                                          )

    phage_experimenter_name = forms.CharField(label='Experimenter Name',
                                              max_length=30,
                                              required=True,
                                              help_text='Required.',
                                              widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                            'autocomplete': 'off',
                                                                            'size': '100',
                                                                            'style': 'font-size: small',
                                                                            })
                                              )

    phage_CPT_id = forms.CharField(label='CPT id',
                                   max_length=30,
                                   required=False,
                                   help_text='Optional.',
                                   widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                 'autocomplete': 'off',
                                                                 'size': '100',
                                                                 'style': 'font-size: small',
                                                                 })
                                   )

    phage_isolator_loc = forms.CharField(label='Isolator Location',
                                         max_length=5000,
                                         required=True,
                                         help_text='Required.',
                                         widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                       'autocomplete': 'off',
                                                                       'size': '100',
                                                                       'style': 'font-size: small',
                                                                       })
                                         )


    class Meta:
        model = PhageData
        fields = ('phage_name', 'phage_host_name',
                  'phage_isolator_name', 'phage_experimenter_name',
                  'phage_CPT_id', 'phage_isolator_loc',
                  )


    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'accordion'
    helper.field_class = 'accordion'
    #helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
    #helper.add_input(Reset('cancel', 'Clear', css_class='btn-warning'))
    helper.layout = Layout(
        HTML("<button class='accordion'>Phage Data</button>"),
        HTML("<div class='panel'>"),
        HTML("<br>"),
        Div('phage_name', 'phage_host_name', 'phage_CPT_id'),
        HTML("</div>"),
        HTML("<button class='accordion'>Researcher Details</button>"),
        HTML("<div class='panel'>"),
        HTML("<br>"),
        Div('phage_isolator_name', 'phage_experimenter_name'),
        HTML("</div>"),
        HTML("<button class='accordion'>Research Information</button>"),
        HTML("<div class='panel'>"),
        HTML("<br>"),
        Div('phage_isolator_loc'),
        HTML("</div>"),
        HTML("<button class='accordion'>Images, Documents & Links</button>"),
        HTML("<div class='panel'>"),
        HTML("<br>"),
        HTML("{{ link_formset.management_form }}"),
        HTML("{% for link_form in link_formset %} <div class='link-formset'> {{ link_form.link }} </div> {% endfor %}"),
        HTML("<script> $('.link-formset').formset({addText: 'add link', deleteText: 'remove'});</script>"),
        HTML("</div>"),
        HTML("<button class='accordion'>Additional Information</button>"),
        HTML("<div class='panel'>"),
        HTML("<br>"),
        Div('phage_isolator_loc'),
        HTML("</div>"),
        HTML("<br><br>"),
        HTML("<input type = 'submit' value = 'Submit' class ='btn-success'/>")
    )


class LinkForm(forms.Form):
    link = forms.CharField(label='URL',
                                      max_length=5000,
                                      required=False,
                                      help_text='',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )



class AForm(forms.Form):
    image = forms.ImageField(label='Upload Image', required=False, widget=forms.FileInput())

    doc = forms.FileField(label='Upload File', required=False, widget=forms.FileInput())



class AIForm(forms.Form):
    link = forms.CharField(label='URL',
                                      max_length=5000,
                                      required=False,
                                      help_text='',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )

class Edit_Phage_DataForm(forms.ModelForm):
    class Meta:
        model = PhageData
        fields = ('phage_name', 'phage_host_name',)

class Edit_ResearcherForm(forms.ModelForm):
    class Meta:
        model = PhageData
        fields = ("phage_isolator_name", "phage_experimenter_name",)

class Edit_ResearchForm(forms.ModelForm):
    class Meta:
        model = PhageData
        fields = ("phage_CPT_id", "phage_isolator_loc",)