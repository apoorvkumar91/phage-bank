from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from PhageBank.core.forms import SignUpForm, AddPhageForm, AddPeopleForm


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
    context = {
        'PhageForm': AddPhageForm(),
        'PeopleForm': AddPeopleForm()
    }
    if request.method == 'POST':
        formA = AddPhageForm(request.POST)
        formC = AddPeopleForm(request.POST)
        if formA.is_valid() and formC.is_valid():
            formA.save()
            formC.save()

            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('home')
        else:
            formA = AddPhageForm(request.POST)
            formC = AddPeopleForm(request.POST)
    return render(request, 'addphage.html',
                              context)


