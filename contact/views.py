from django.shortcuts import render
from django.http import HttpResponse

#def index(request):
#    return render(request, 'contact/contact.html');
#    #return HttpResponse("<h2> Hi </h2>")
#    
def index(request):
    return render(request, 'contact/contact.html', {'content':['In case of any questions / suggestions, email me at:','cory.maughmer@tamu.edu']});
