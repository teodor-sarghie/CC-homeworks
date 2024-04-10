from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def health(request):
    return HttpResponse(status=200)
