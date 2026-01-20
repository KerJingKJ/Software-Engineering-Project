from django.shortcuts import render, redirect, get_object_or_404
from .models import Application
from .forms import ApplicationForm
# Create your views here.
# views.py

def index(response):
    return render(response, "student/student.html", {})

def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()  # save() will set status='Pending'
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm()
    
    return render(request, 'applications/create.html', {'form': form})


def edit_application(request, id):
    application = get_object_or_404(Application, pk=id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_detail', pk=application.id)
    else:
        form = ApplicationForm(instance=application)
    
    return render(request, 'applications/edit.html', {'form': form})