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
    # def clean(self):
    # # To keep the main validation and error messages
    #     super(DashboardPanelForm, self).clean()

    # # Now it's time to add your custom validation
    #     if len(self.cleaned_data['password']) < 10:
    #          self._errors['password']='your password\'s length is too short'
    #          # you may also use the below line to custom your error message, but it doesn't work with me for some reason
    #          raise forms.ValidationError('Your password is too short')
    #     token = os.getenv('GH_ACCESS_TOKEN')
    #     g = Github(token)
       
    #     try:
    #         user = g.get_user(self.github_username)
    #     except:
    #         raise Exception("user does not exist")
    #     # if repo:
    #     try:
    #         repo = user.get_repo(self.repo_name)
    #     except:
    #         raise Exception("repo does not exist")


"""simple landing page view.  main content consists of additional button links for the repository data pages"""
def home(request):
    context = {}
    # if user:
    dashboards = DashboardPanel.objects.all()
    context['dashboards'] = dashboards
    # #     auth.login(request, user)
    # print(dashboards)

    # 'home_active' is a templated variable in template. set to 'active' to set home page nav link to active class
    context['home_active'] = 'active'
    return render(request, 'pages/home.html', context)

def panel_details(request, dash_id):
    context = {}
    panel = DashboardPanel.objects.get(id=dash_id)
    context['panel'] = panel 
    return render(request, 'pages/details.html', context)
    
def panel_collections(request, user_id):
    dashboards = None
    if request.POST:
        form = PanelCollectionForm(request.POST)
        if form.is_valid():
            new_dashboard = form.save(commit=False)
            new_dashboard.creator = User.objects.get(id=request.user.id)
            new_dashboard.save()
    else:
        form = PanelCollectionForm()
    if request.user:
        dashboards = PanelCollection.objects.filter(creator=request.user.id)
    context = {'form':form, 'dashboards':dashboards}
    return render(request,'pages/dashboards.html',context)

def user_panels(request, user_id):
    panels = None
    if request.POST:
        form = DashboardPanelForm(request.POST)
        if form.is_valid():
            new_panel = form.save(commit=False)
            new_panel.creator = User.objects.get(id=request.user.id)
            new_panel.save()
         
    else: 
        form = DashboardPanelForm()
    if request.user:
        panels = DashboardPanel.objects.filter(creator=request.user.id)
    context = {'panels': panels, 'form': form}
    return render(request, 'pages/panels.html', context)