from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h> this is html  </h>   \
        Hello, world. You're at the polls index.    \
            <p> this is label </p>  ")
# Create your views here.
