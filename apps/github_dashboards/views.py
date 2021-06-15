"""imports of libraries, functions, and modules needed for views.py"""
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib import auth
"""from modules/*, custom modules containing utility fnctions and form classes"""
from .modules import custom_utils
from .models import DashboardPanel, PanelCollection
from apps.accounts.models import User
from django import forms
from .modules import custom_utils
import os
from django.contrib import messages
from github import Github
#from .modules import custom_forms

"""load any needed env variables"""
load_dotenv()

class DashboardPanelForm(forms.ModelForm):
    class Meta:
        model = DashboardPanel
        fields = ['panel_type', 'github_username', 'repo_name', 'description', 'panel_style', 'panel_size']

class PanelCollectionForm(forms.ModelForm):
    class Meta:
        model = PanelCollection
        fields = ['title', 'description', 'panels']

"""simple landing page view.  main content consists of additional button links for the repository data pages"""
def home(request):
    context = {}
    dashboards = DashboardPanel.objects.all()
    context['dashboards'] = dashboards
    # 'home_active' is a templated variable in template. set to 'active' to set home page nav link to active class
    context['home_active'] = 'active'
    return render(request, 'pages/home.html', context)

def edit_panel(request, panel_id):
    
    context = {}
    panel = DashboardPanel.objects.get(id=panel_id)
    if request.POST:
        form = DashboardPanelForm(request.POST, instance=panel)
        if form.is_valid():
            form.save()
        messages.success(request, 'Panel ("panel.github.user_name/panel.repo_name") was successfully updated!')
        return redirect('user_panels', request.user.id)
    form = DashboardPanelForm(instance=panel)
    if form.is_valid():
        form.save()
    context['form']= form
    panels = DashboardPanel.objects.filter(creator=request.user.id)
    context['panels']=panels
    print(context)
    context['panel_id']=panel_id
    return render(request, 'pages/panels.html', context)
    return render(request, 'pages/panels.html', context)

def panel_details(request, dash_id):
    context = {}
    panel = DashboardPanel.objects.get(id=dash_id)
    context['panel'] = panel 
    return render(request, 'pages/details.html', context)

    
def panel_collections(request, user_id=None):
    dashboards = None
    form = None
    if user_id:
        if request.POST:
            form = PanelCollectionForm(request.POST)
            if form.is_valid():
                new_dashboard = form.save(commit=False)
                new_dashboard.creator = User.objects.get(id=request.user.id)
                new_dashboard.save()
        else:
            form = PanelCollectionForm()
       
        dashboards = PanelCollection.objects.filter(creator=request.user.id)
    else:
        dashboards = []

    context = {'form':form, 'dashboards':dashboards}
    return render(request,'pages/dashboards.html',context)


def user_panels(request, user_id=None):
    
    form = None  
    panels = None
    if user_id:
        if request.POST:
            form = DashboardPanelForm(request.POST)

            if form.is_valid():
                new_panel = form.save(commit=False)
                new_panel.creator = User.objects.get(id=request.user.id)
                new_panel.save()
             
        else: 
            form = DashboardPanelForm()
        panels = DashboardPanel.objects.filter(creator=request.user.id)
    else:
        panels = []

    context = {'panels': panels, 'form': form}
    return render(request, 'pages/panels.html', context)