from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


# Create your views here.
def product_list(request: HttpRequest):
    return HttpResponse("안녕")
