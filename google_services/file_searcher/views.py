from django.shortcuts import render
import requests
import os
from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError

from Drives.GoogleDrive import GoogleDrive
import pprint
import json
from django.conf import settings
from datetime import datetime

def home(request):
    return render(request, 'home.html')



def add_file(request):
    msg = ''
    if request.method == 'POST':
        msg = ''
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            gd = GoogleDrive()
            gd.connect()
            file_id = gd.upload_file_directly(uploaded_file, uploaded_file.name, mime_type=uploaded_file.content_type)
            msg = file_id  
    return render(request, 'add_file.html', {'msg':msg})
  