from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from PhageBank.core.forms import SignUpForm, AddPhageForm
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
        form = AddPhageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPhageForm()
    return render(request, 'addphage.html',
                  {'form': form})

def viewphages(request):
    query_results = PhageData.objects.all()
    return render(request, 'viewphages.html', {'query_results': query_results})