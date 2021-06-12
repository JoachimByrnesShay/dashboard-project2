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
#from .modules import custom_forms

"""load any needed env variables"""
load_dotenv()

class DashboardPanelForm(forms.ModelForm):
    class Meta:
        model = DashboardPanel
        fields = ['panel_type', 'github_username', 'repo_name', 'description', 'panel_style', 'panel_size']
       

 


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
    

def user_panels(request, user_id):
    
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