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
            request.session['detail'] = kaamdar(uploaded_file_url)
            return redirect('data_extraction')
    return render(request,'resumeparser.html')

def data_extraction(request):
    return render(request,'dataextraction.html')