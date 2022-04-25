import json
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from parserapp.parser import kaamdar

# Create your views here.
def index(request):
    return render(request,'home.html')

def resume_parser(request):
    if request.method == 'POST':
        if len(request.FILES)!=0:
            file = request.FILES.get('file')
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            data = kaamdar(uploaded_file_url)
            # print(data[0]["name"])
            request.session['name'] = data[0]["name"]
            request.session['email'] = data[0]["email"]
            request.session['mobile_number'] = data[0]["mobile_number"]
            request.session['technical_skills'] = data[0]["technical_skills"]
            request.session['soft_skills'] = data[0]["soft_skills"]
            request.session['education'] = data[0]["education"]
            request.session['languages'] = data[0]["languages"]
            request.session['experience'] = data[0]["experience"]
            request.session['address'] = data[0]["address"]
            return redirect('data_extraction')
    return render(request,'resumeparser.html')

def data_extraction(request):
    return render(request,'dataextraction.html')

def faq(request):
    return render(request,'faq.html')

def terms(request):
    return render(request,'terms.html')

def login(request):
    return render(request,'login.html')