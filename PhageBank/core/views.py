from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import csv
from django.conf import settings
from io import StringIO
from io import TextIOWrapper
from PhageBank.core.forms import Add_ResearchForm, AForm, AIForm, Edit_Phage_DataForm, Edit_ResearcherForm, Edit_ResearchForm, Edit_IsolationDataForm, Edit_Experiment_Form
from PhageBank.core.forms import SignUpForm, UploadFileForm, LinkForm, LoginForm, Add_Phage_DataForm, Add_ResearcherForm, Add_Experiment_Form,Isolation_Form
from PhageBank.core.models import PhageData, PreData, ExperimentData, IsolationData
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.template import RequestContext
from django.contrib.messages import get_messages

import os
from csvvalidator import *
import datetime
import sqlite3
import pandas as pd

def new_index(request):
    return render(request, 'new_index.html',{'login_status': request.user.is_authenticated(),
                                          'username': request.user.username
                                          })

def logged_in_index(request):
    return render(request, 'logged_in_index.html',{'login_status': request.user.is_authenticated(),
                                                   'username': request.user.username
                                          })
def mylogout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.', extra_tags='alert')
    return render(request, 'new_index.html', {'login_status': request.user.is_authenticated(),
                                              'username': request.user.username
                                              })
@login_required
def add_phage(request):
    return render(request, 'add_phage.html')

def signup(request):
    data = dict()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SignUpForm()

    context = {'form': form}
    data['html_form'] = render_to_string('partial_signup.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

def mylogin(request):
    msg = dict()
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                msg['form_is_valid'] = True
            else:
                msg['form_is_valid'] = False
        else:
            form = LoginForm()
    context = {'form': form}
    msg['html_form'] = render_to_string('partial_login.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(msg)


def handle_uploaded_file(f, dest):
    with open(dest, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#Fill the model object in similar fashion
def fillExpObject(expform, phage):
    exp =  ExperimentData.objects.create(expkey=phage)
    exp.expkey = phage
    exp.owner = expform.cleaned_data.get('owner')
    exp.timestamp = expform.cleaned_data.get('timestamp')
    exp.category = expform.cleaned_data.get('category')
    exp.short_name = expform.cleaned_data.get('short_name')
    exp.full_name = expform.cleaned_data.get('full_name')
    exp.methods = expform.cleaned_data.get('methods')
    exp.results = expform.cleaned_data.get('results')
    exp.save()

def fillExpObjectedit(expform, exp):
    exp.owner = expform.cleaned_data.get('owner')
    exp.timestamp = expform.cleaned_data.get('timestamp')
    exp.category = expform.cleaned_data.get('category')
    exp.short_name = expform.cleaned_data.get('short_name')
    exp.full_name = expform.cleaned_data.get('full_name')
    exp.methods = expform.cleaned_data.get('methods')
    exp.results = expform.cleaned_data.get('results')
    exp.save()

def fillIsoltionObject(isoform, phage):
    iso = IsolationData.objects.create(isokey=phage)
    iso.isokey = phage
    iso.owner_name = isoform.cleaned_data.get('owner_name')
    iso.location = isoform.cleaned_data.get('location')
    iso.type = isoform.cleaned_data.get('type')
    iso.TimeStamp = isoform.cleaned_data.get('timestamp')
    iso.save()

def fillIsoltionObjectedit(isoform, iso):
    iso.owner_name = isoform.cleaned_data.get('owner_name')
    iso.location = isoform.cleaned_data.get('location')
    iso.type = isoform.cleaned_data.get('type')
    iso.TimeStamp = isoform.cleaned_data.get('TimeStamp')
    iso.save()

@login_required
def add_phage(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pform = Add_Phage_DataForm(request.POST)
            rrform = Add_ResearcherForm(request.POST)
            rform = Add_ResearchForm(request.POST)
            expform = Add_Experiment_Form(request.POST)
            isoform = Isolation_Form(request.POST)
            aform = AForm(request.POST, request.FILES)
            aiform = AIForm(request.POST)
            if pform.is_valid() and rrform.is_valid() and rform.is_valid() and expform.is_valid() and isoform.is_valid() \
                    and aform.is_valid() and aiform.is_valid():
                pform.save()
                phagename = pform.cleaned_data.get('phage_name')
                phage = PhageData.objects.get(phage_name=phagename)
                phage.phage_CPT_id = rform.cleaned_data.get('phage_CPT_id')
                phage.phage_isolator_loc = rform.cleaned_data.get('phage_isolator_loc')
                phage.phage_all_links = aiform.cleaned_data.get('link')
                phage.phage_isolator_name = rrform.cleaned_data.get('phage_isolator_name')
                phage.phage_experimenter_name = rrform.cleaned_data.get('phage_experimenter_name')
                phage.phage_submitted_user = request.user.username
                phage.phage_lab = rrform.cleaned_data.get('phage_lab')
                print(phage.phage_lab)
                phage.save()
                fillIsoltionObject(isoform, phage)
                print(phage.iso_phageName.all().values())
                fillExpObject(expform, phage)
                print (phage.PName.all().values())
                # print(phage.phage_submitted_user)
                phagedoc = aform.cleaned_data.get('doc')
                phageimage = aform.cleaned_data.get('image')
                dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phagename)
                docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", phagename)
                try:
                    os.mkdir(dest_dir)
                    os.mkdir(docs_dest_dir)
                except:
                    pass
                dest = os.path.join(dest_dir, str(phageimage))
                docsdest = os.path.join(docs_dest_dir, str(phagedoc))
                if phageimage is None:
                    pass
                else:
                    handle_uploaded_file(phageimage, dest)
                if phagedoc is None:
                    pass
                else:
                    handle_uploaded_file(phagedoc, docsdest)
                query_results = PhageData.objects.all()
                return render(request, 'view_phages.html', {'add_status':'true','query_results':query_results}  )
            else:
                pform = Add_Phage_DataForm()
                rrform = Add_ResearcherForm()
                rform = Add_ResearchForm()
                expform = Add_Experiment_Form()
                isoform = Isolation_Form()
                aform = AForm()
                aiform = AIForm()
                return render(request, 'add_phage.html', {'pform': pform,
                                                          'rrform': rrform,
                                                          'rform': rform,
                                                          'expform': expform,
                                                          'isoform': isoform,
                                                          'aform': aform,
                                                          'aiform': aiform,
                                                          'login_status': request.user.is_authenticated(),
                                                          'username': request.user.username,
                                                         })
        else:
            pform = Add_Phage_DataForm()
            rrform = Add_ResearcherForm()
            rform = Add_ResearchForm()
            expform = Add_Experiment_Form()
            isoform = Isolation_Form()
            aform = AForm()
            aiform = AIForm()
            return render(request, 'add_phage.html', {'pform': pform,
                                                      'rrform': rrform,
                                                      'rform': rform,
                                                      'expform': expform,
                                                      'isoform':isoform,
                                                      'aform': aform,
                                                      'aiform': aiform,
                                                      'login_status': request.user.is_authenticated(),
                                                      'username': request.user.username,
                                                     })
    else:
        return render(request,'Login.html',
                      {'login_status': request.user.is_authenticated()
                       })

#this form show the phages per user
def my_phages(request):
    query_results = PhageData.objects.filter(phage_submitted_user=request.user.username)
    return render(request, 'view_phages.html', {'query_results': query_results,
                                                'edit_status':'false','add_status':'false',
                                                'delete_status':'false',
                                               'login_status': request.user.is_authenticated(),
                                               'username': request.user.username
                                               })
#this form shows all the phages
def view_phages(request):

    query_results = PhageData.objects.all()
    return render(request, 'view_phages.html', {'query_results': query_results,
                                                'edit_status':'false','add_status':'false',
                                                'delete_status':'false',
                                               'login_status': request.user.is_authenticated(),
                                               'username': request.user.username
                                               })
#this form shows a particular phage
def view_phage(request):
    phageName = request.GET.get('name')
    phage = PhageData.objects.get(phage_name=phageName)
    previous_names = phage.PhageName.all()
    expdata = phage.PName.all()
    isodata = phage.iso_phageName.all()
    dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phageName)
    list_path=[]
    count = 0;
    for filename in os.listdir(dest_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            list_path.append(filename)
            count=count+1;
            continue
        else:
            continue
    print(list_path)
    return render(request, 'view_phage.html', {'item': phage,'previous_names':previous_names,'expdata':expdata,'isodata':isodata,
                                              'login_status': request.user.is_authenticated(),'dest_dir':list_path,'count':count,
                                              'username': request.user.username
                                              })

@login_required
def deletephages(request):
    if request.user.is_authenticated():
        x = request.GET.get('name')
        dest_dir = os.path.join(settings.MEDIA_ROOT, "images", x)
        docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", x)
        try:
            os.rmdir(dest_dir)
            os.rmdir(docs_dest_dir)
        except:
            pass
        phage = PhageData.objects.get(phage_name=x).delete()
        query_results = PhageData.objects.all()

        return render(request, 'view_phages.html', {'query_results': query_results,'delete_status':'true',
                                               'login_status': request.user.is_authenticated(),
                                               'username': request.user.username
                                               })
    else:
        #messages.error(request,'Login or signup first!')
        return render(request,'login.html',
                      {'login_status': request.user.is_authenticated()
                       })

@login_required
def editPhage(request):
    if request.user.is_authenticated():
        name = request.GET.get('name')
        phage = PhageData.objects.get(phage_name = name)
        isodata = IsolationData.objects.filter(isokey = phage)
        expdata = ExperimentData.objects.filter(expkey = phage)
        last = isodata.latest('id')
        last_exp = expdata.latest('id')
        print(last_exp.owner)
        print(last.owner_name)
        pform = Edit_Phage_DataForm(request.POST, instance=phage, initial = {'phage_name':phage.phage_name })
        rrform = Edit_ResearcherForm(request.POST, instance=phage)
        rform = Edit_ResearchForm(request.POST, instance=phage)
        isoform = Edit_IsolationDataForm(request.POST)
        expform = Edit_Experiment_Form(request.POST)
        aform = AForm(request.POST, request.FILES)
        aiform = AIForm(request.POST)
        if request.method=="POST":
            if pform.is_valid() and rrform.is_valid() and rform.is_valid() and aform.is_valid() and aiform.is_valid()\
                    and isoform.is_valid() and expform.is_valid():
                phage.phage_name = pform.cleaned_data.get('phage_name')
                if(name!=phage.phage_name and PreData.objects.filter(phagename = name).count()==0):
                    obj = PreData.objects.create(testkey=phage)
                    obj.testkey = phage
                    obj.phagename = name
                    print (obj.phagename)
                    obj.save()
                    print (phage.PhageName.all().values())
                #phage = PhageData.objects.get(phage_name=phagename)
                phage.phage_isolator_name = rrform.cleaned_data.get('phage_isolator_name')
                phage.phage_experimenter_name = rrform.cleaned_data.get('phage_experimenter_name')
                phage.phage_CPT_id = rform.cleaned_data.get('phage_CPT_id')
                phage.phage_isolator_loc = rform.cleaned_data.get('phage_isolator_loc')
                phage.phage_all_links = aiform.cleaned_data.get('link')
                phage.phage_lab = rrform.cleaned_data.get('phage_lab')
                print(phage.phage_lab)
                #isolator_data = phage.iso_phageName.objects.latest(iso_phageName)
                pform.save()
                phage.save()
                #last.delete()
                fillExpObjectedit(expform, last_exp)
                fillIsoltionObjectedit(isoform, last)
                phagedoc = aform.cleaned_data.get('doc')
                phageimage = aform.cleaned_data.get('image')
                dest_dir_old = os.path.join(settings.MEDIA_ROOT, "images", name)
                docs_dest_dir_old = os.path.join(settings.MEDIA_ROOT, "docs", name)
                dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phage.phage_name)
                docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", phage.phage_name)
                print(dest_dir_old)
                print(dest_dir and name!=phage.phage_name)
                try:
                    os.rename(dest_dir_old,dest_dir)
                    os.rename(docs_dest_dir_old,docs_dest_dir)
                except:
                   pass
                dest = os.path.join(dest_dir, str(phageimage))
                docsdest = os.path.join(docs_dest_dir, str(phagedoc))
                if phageimage is None:
                    pass
                else:
                    handle_uploaded_file(phageimage, dest)
                if phagedoc is None:
                    pass
                else:
                    handle_uploaded_file(phagedoc, docsdest)
                query_results = PhageData.objects.all()
                return render(request, 'view_phages.html', {'edit_status':'true','query_results':query_results}  )
            else:
                phage = PhageData.objects.get(phage_name=name)
                print (phage.phage_host_name)
                phage.save()
                return render(request, 'EditPhage.html', {'item': phage,
                                                          'pform': pform,
                                                          'rrform': rrform,'expform':expform,
                                                          'rform': rform,
                                                          'aform': aform,
                                                          'aiform': aiform,
                                                          'isoform':isoform,'iso':last,'exp':last_exp,
                                                          'login_status': request.user.is_authenticated(),
                                                          'username': request.user.username,
                                                         })
        else:
            pform = Edit_Phage_DataForm(request.POST, instance=phage)
            rrform = Edit_ResearcherForm(request.POST, instance=phage)
            rform = Edit_ResearchForm(request.POST, instance=phage)
            isoform = Edit_IsolationDataForm(request.POST)
            expform = Edit_Experiment_Form(request.POST)
            aform = AForm()
            aiform = AIForm()
            return render(request, 'EditPhage.html', {'item': phage,
                                                      'pform': pform,
                                                      'rrform': rrform,
                                                      'rform': rform,
                                                      'aform': aform,
                                                      'aiform': aiform, 'isoform' : isoform,'expform':expform,
                                                      'iso':last,
                                                      'exp': last_exp,
                                                      'login_status': request.user.is_authenticated(),
                                                      'username': request.user.username,
                                                     })
    else:
        return render(request,'Login.html',
                      {'login_status': request.user.is_authenticated()
                       })

def func(phagename):
    dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phagename)
    docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", phagename)
    try:
        os.mkdir(dest_dir)
        os.mkdir(docs_dest_dir)
    except:
        pass
    print(dest_dir)
def populate(reader, request):
    fields = reader.fieldnames
    for row in reader:
        flag = 0
        obj = PhageData.objects.create()
        if 'phage_name' in fields:
            obj.phage_name = row['phage_name']
            flag = 1
        if 'phage_host_name' in fields:
            obj.phage_host_name = row['phage_host_name']
            flag = 1
        if 'phage_isolator_name' in fields:
            obj.phage_isolator_name = row['phage_isolator_name']
            flag = 1
        if 'phage_experimenter_name' in fields:
            obj.phage_experimenter_name = row['phage_experimenter_name']
            flag = 1
        if 'phage_CPT_id' in fields:
            obj.phage_CPT_id = row['phage_CPT_id']
            flag = 1
        if 'phage_isolator_loc' in fields:
            flag = 1
            obj.phage_isolator_loc = row['phage_isolator_loc']
        obj.phage_submitted_user = request.user.username

        if flag == 0:
            obj.delete()
        else:
            obj.save()
            func(obj.phage_name)


@user_passes_test(lambda u: u.is_superuser)
def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            paramFile = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
            reader = csv.DictReader(paramFile,delimiter=';',skipinitialspace=True,)
            populate(reader, request)
            query_results = PhageData.objects.all()
            return render(request, 'view_phages.html', {'query_results': query_results,
                                                        'edit_status': 'false', 'add_status': 'false',
                                                        'delete_status': 'false',
                                                        'login_status': request.user.is_authenticated(),
                                                        'username': request.user.username
                                                        })
    else:
        form = UploadFileForm()
    return render(request, 'model_form_upload.html', {'form': form})


def contact(request):
    return render(request,'contact.html',{'content':['In case of any questions / suggestions, email me at:','cory.maughmer@tamu.edu'],
                                          'login_status': request.user.is_authenticated(),
                                          'username': request.user.username
                                          })

def header(request):
    return render(request, 'header.html')