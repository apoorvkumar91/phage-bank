from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import csv
from io import StringIO
from io import TextIOWrapper
from PhageBank.core.forms import SignUpForm, AddPhageForm, UploadFileForm
from PhageBank.core.models import PhageData
from csvvalidator import *
import datetime
import sqlite3
import pandas as pd

@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def addphage(request):
    if request.method == 'POST':
        phageform = AddPhageForm(request.POST)
        if phageform.is_valid():
            phageform.save()
            return redirect('home')
    else:
        phageform = AddPhageForm()
        return render(request, 'addphage.html', {'form': phageform})

def viewphages(request):
    query_results = PhageData.objects.all()
    return render(request, 'viewphages.html', {'query_results': query_results})

def viewPhage(request):
    phageName = request.GET.get('name')
    phage = PhageData.objects.get(phage_name=phageName)
    return render(request, 'viewPhage.html', {'item': phage})

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


def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            paramFile = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
            reader = csv.DictReader(paramFile,delimiter=';',skipinitialspace=True,)
            populate(reader, request)
            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, 'model_form_upload.html', {'form': form})

