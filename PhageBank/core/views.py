from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import csv
import io
from PhageBank.core.forms import SignUpForm, AddPhageForm, UploadFileForm
from PhageBank.core.models import PhageData

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

def handle_uploaded_file(uploadedfile):
    csv_file = uploadedfile
    decoded_file = csv_file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    for line in csv.reader(io_string, delimiter=','):
        PhageData.objects.create(phage_name=line[0],phage_host_name=line[1],phage_isolator_name=line[2],
                                 phage_experimenter_name=line[3],phage_CPT_id=line[4],phage_isolator_loc=line[5])
        print(line)

def viewphages(request):
    query_results = PhageData.objects.all()
    return render(request, 'viewphages.html', {'query_results': query_results})

def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, 'model_form_upload.html', {'form': form})

