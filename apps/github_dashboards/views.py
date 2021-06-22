"""imports of libraries, functions, and modules needed for views.py"""
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib import auth
"""from modules/*, custom modules containing utility fnctions and form classes"""
from .modules import custom_utils
from .models import Panel, PanelsCollection
from apps.accounts.models import User
from django import forms
from .modules import custom_utils
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from github import Github
from .modules.custom_utils import clean_repo_name
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core import validators
#from .modules import custom_forms

"""load any needed env variables"""
load_dotenv()


class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['panel_type', 'github_username', 'repo_name', 'description', 'panel_style', 'panel_size', 'id']
    
    #https://stackoverflow.com/questions/18330622/django-modelform-conditional-validation


    def __init__(self, *args, **kwargs):
        super(PanelForm, self).__init__(*args, **kwargs)
        panel_type = self.data.get("panel_type")
        self.fields['panel_style'].initial = 'DefaultStyle'

  

class PanelsCollectionForm(forms.ModelForm):
    class Meta:
        model = PanelsCollection
        fields = ['title', 'description', 'panels']

"""simple landing page view.  main content consists of additional button links for the repository data pages"""
def home(request):
    context = {}
    dashboards = Panel.objects.all()
    context['dashboards'] = dashboards
    # 'home_active' is a templated variable in template. set to 'active' to set home page nav link to active class
    context['home_active'] = 'active'
    return render(request, 'pages/home.html', context)

@login_required
def delete_panel(request, panel_id):
    this_panel = Panel.objects.get(id=panel_id)
     
    repo_name = '' if this_panel.repo_name == 'TableOfRepos' else this_panel.repo_name
    user_name = this_panel.github_username
    this_panel.delete()
    messages.warning(request, f"Panel: {user_name}/{repo_name} was successfully deleted!" )
    return redirect('user_panels', request.user.id)

@login_required
def delete_collection(request, collection_id):
    collection = PanelsCollection.objects.get(id=collection_id)
    collection.delete()
    messages.warning(request, 'Collection: ("collection.title") was successfully deleted!' )
    return redirect('panel_collections', request.user.id)

@login_required
def edit_panel(request, panel_id):
    panels = Panel.objects.filter(creator=request.user.id).order_by('id')
    context = {}
    context['panels_active'] = 'active'
    panel = Panel.objects.get(id=panel_id)
    form = PanelForm(instance=panel)
    if request.POST:
        form = PanelForm(request.POST, instance=panel)
        if form.is_valid():
            form.save()
            repo_name = '' if panel.github_username is None else panel.github_username
            messages.success(request, f"Panel '{panel.github_username}/{repo_name}' was successfully updated!")
            return redirect('user_panels', request.user.id)
    context['form']= form
    context['panels']=panels
    return render(request, 'pages/panels.html', context)

@login_required
def edit_collection(request, collection_id):
    print(collection_id)
    context = {}
    collections = PanelsCollection.objects.filter(creator=request.user.id)
    collection = PanelsCollection.objects.get(id=collection_id)
    print(collection)
    
    form = PanelsCollectionForm(instance=collection)
    if request.POST:
        form = PanelsCollectionForm(request.POST, instance=collection)
        if form.is_valid():
            this_collection = form.save(commit=False)
            this_collection.save()
            form.save_m2m()
            form.save()
            messages.success(request, f"Dashboard '{collection.title}' was successfully updated!")
            
            #return render(request, 'pages/collections.html', context)
            return redirect('user_collections')
        
            #return render(request, 'pages/collections.html', {'form': form})   
    
    #.order_by('id')
    context['form'] = form 
    context['collections'] = collections
    context['user_id'] = request.user.id
    return render(request, 'pages/collections.html',context)   


    

    


def panel_details(request, dash_id):
    context = {}
    panel = Panel.objects.get(id=dash_id)
    context['panel'] = panel 
    return render(request, 'pages/details.html', context)



@login_required
def user_collections(request, user_id=None):
    form = PanelsCollectionForm()
    if user_id:
       
        if request.POST:
            print(request.POST)
            form = PanelsCollectionForm(request.POST)
            if form.is_valid():
                new_collection = form.save(commit=False)
                new_collection.creator = User.objects.get(id=request.user.id)
                new_collection.save()
                form.save_m2m()
                messages.error(request, "Successfully created new panel collection!")

       
            
            
    collections = PanelsCollection.objects.filter(creator=request.user)
        
 
    context = {'form':form, 'collections':collections, 'collections_active': 'active'}
    return render(request,'pages/collections.html',context)


@login_required
def user_panels(request, user_id=None):
    panels_active = 'active'
    panels = Panel.objects.filter(creator=request.user.id).order_by('id')
    context = {}
    
   
    
    form = PanelForm()
    if request.user.id:
        if request.POST:
            form = PanelForm(request.POST)

            if form.is_valid():
                print('form_valid')
                new_panel = form.save(commit=False)
                new_panel.creator = User.objects.get(id=request.user.id)
                new_panel.save()
                messages.success(request, f"Successfully added this {new_panel.panel_type}: '{new_panel}")
                
                #context['user_id'] = request.user.id
               
                return redirect('user_panels')

    else:
        panels = []
    context['panels'] = panels
    context['form'] = form
    context['panels_active'] = panels_active
   # context = {'panels': panels, 'form': form, 'panels_active': 'active'}
    return render(request, 'pages/panels.html', context)

