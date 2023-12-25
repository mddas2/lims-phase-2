from django.http  import HttpResponse
from django.shortcuts import render
from .form import MessageForm

def index_form(request):
    form  = MessageForm()
    data = {
        'form':form,
    }
    # return HttpResponse("hello fomr")
    return render(request,"report.html",data)