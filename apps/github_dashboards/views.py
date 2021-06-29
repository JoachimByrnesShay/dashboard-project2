"""imports of libraries, functions, and modules needed for views.py"""
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from apps.accounts.models import User
from .models import Panel, PanelsCollection


class PanelForm(forms.ModelForm):
    """ use of modelform to return form based on Panel model """
    class Meta:
        model = Panel
        fields = ['panel_type', 'github_username', 'repo_name', 'description', 'panel_style', 'panel_size', 'id']
    

class PanelsCollectionForm(forms.ModelForm):
    """ use of modelform to return form based on PanelsCollection model """
    class Meta:
        model = PanelsCollection
        fields = ['title', 'description', 'panels']


def home(request):
    """landing page related view. obtains all panels and passes them for display in rows by home template. main content consists of additional button links for the repository data pages"""
    context = {}
    panels = Panel.objects.all()
    context['panels'] = panels
    # 'home_active' is a templated variable in template. set to 'active' to control css for active page link for main pages for by setting home nav link to active class
    context['home_active'] = 'active'
    return render(request, 'pages/home.html', context)


# login required is used to control access in the app to all create (other than create new user), update, delete related views, and to read-related views that are not general but are BOTH user specific AND linked to editability
@login_required
def user_panels(request):
    """ get logged-in users panels and display in rows, with new panel creation form.  the associated template but not this view also links exclusively to URLs for edit view (with corresponding form and its specific data handling) and delete view"""

    # set active link to template associated with this view, i.e. panels.html
    panels_active = 'active'
    # obtain all panels for logged-in user, order_by id as without doing so results in a default ordering by date_created/date_updated, which results in an edited panel upon submit being moved suddenly out of place per the user's perspective (it gets placed at end of last row because it is the most recently updated object) 
    panels = Panel.objects.filter(creator=request.user.id).order_by('id')
    context = {}
    
    # by default, the template associated with this view will render a form with only placeholders and no populated data.
    form = PanelForm()

    # if request.POST, a new panel is being created, cleaned and saved below.  
    if request.POST:
        form = PanelForm(request.POST)

        if form.is_valid():

            # commit=False as we are relying on request data and not a 2nd argument to obtain creator.id, which we add to the instance manually
            new_panel = form.save(commit=False)
            new_panel.creator = User.objects.get(id=request.user.id)
            new_panel.save()
            messages.success(request, f"Successfully added this {new_panel.panel_type}: '{new_panel}")
            return redirect('user_panels')

    context['panels'] = panels
    context['form'] = form
    context['panels_active'] = panels_active
    return render(request, 'pages/panels.html', context)


@login_required
def delete_panel(request, panel_id):
    """called only from URL linked from user_panels template.  retrieves the chosen panel and deletes it. corresponding template offers a modal which provides confirmation guard"""
    this_panel = Panel.objects.get(id=panel_id)     
    this_panel.delete()

    # Panel.__str__ is defined in models to return github-username in case of table or username/reponame in case of other chart
    messages.warning(request, f"Panel: {this_panel} was successfully deleted!" )
    return redirect('user_panels')


@login_required
def edit_panel(request, panel_id):
    """ the edit_panel view/url is exclusively linked from the user_panels url.  links on the panels.html template direct to edit_panel or user_panels views according to whether we need a form for a new object or for an edited existing object"""
    
    # get and order_by id as per user_panels.  edit_panel and user_panels are linked from the same template, which displays rows of panels.  prefer to order_by id rather than updated_at/created_at, as explained in user_panels comments
    panels = Panel.objects.filter(creator=request.user.id).order_by('id')
    context = {}
    # panels.html is the active page, ensure appropriate link is active class. this edit_panel view is only <a> linked from the template returned by the user_panels url
    context['panels_active'] = 'active'
    panel = Panel.objects.get(id=panel_id)

    # by default, the edit form will be populated with the existing data for the instance of the selected panel (which user selected to edit)
    form = PanelForm(instance=panel)
    if request.POST:
        # if the user submits the form, the form data is in the request and is cleaned and saved
        form = PanelForm(request.POST, instance=panel)
        if form.is_valid():
            form.save()
            repo_name = '' if panel.github_username is None else panel.github_username
            messages.success(request, f"Panel '{panel}' was successfully updated!")
            return redirect('user_panels')

    context['form']= form
    context['panels']=panels
    return render(request, 'pages/panels.html', context)


def show_panel(request, panel_id):
    """ this is called by URL linked from several pages which display panel representations in rows.  returns and renders a template which presents a simple detailed view of panel"""
    panel = Panel.objects.get(id=panel_id)
    context = {}
    context['panel'] = panel
    return render(request, 'pages/show_panel.html', context)


@login_required
def user_collections(request):
    """ is called from URL to prepare collections and a form for creating new collection, which are rendered with collections.html """

    # same ordering protocol as with panels.  using Count to annotate each of the retrieved collections with panel_count
    collections = PanelsCollection.objects.filter(creator=request.user).order_by('id').annotate(panel_count=Count('panels'))

    # form for new panel collection
    form = PanelsCollectionForm()
    # if request.POST, then a new collection is being created
    if request.POST:

        form = PanelsCollectionForm(request.POST)
        if form.is_valid():

            new_collection = form.save(commit=False)
            new_collection.creator = User.objects.get(id=request.user.id)
            new_collection.save()
            # in order to save the associated panels with the collection, as it is a many to many relationship, we must additionally call save_m2m() on the form object, elsewise the panels the user selected will not be associated with the collection
            form.save_m2m()
            messages.success(request, "Successfully created new panel collection!")
 
    context = {'form':form, 'collections':collections, 'collections_active': 'active'}
    return render(request,'pages/collections.html',context)

@login_required
def delete_collection(request, collection_id):
    """called only from URL linked from user_collections template.  retrieves the chosen collection and deletes it.  corresponding template offers a modal which provides confirmation guard"""
    collection = PanelsCollection.objects.get(id=collection_id)
    collection.delete()

    # refer to a collection by its title in messaging
    messages.warning(request, f'Collection: ("{collection.title}") was successfully deleted!' )
    return redirect('user_collections')



@login_required
def edit_collection(request, collection_id):
    """ similar to the structure of user_panels/edit_panel, edit_collection and user_collections are called by URL's linked to the same page:  the user_collections URL """
    context = {}
    collections = PanelsCollection.objects.filter(creator=request.user.id).order_by('id')
    this_collection = PanelsCollection.objects.get(id=collection_id)
    
    form = PanelsCollectionForm(instance=this_collection)
    if request.POST:

        form = PanelsCollectionForm(request.POST, instance=this_collection)
        if form.is_valid():

            edited_collection = form.save(commit=False)
            edited_collection.save()
             # in order to save the associated panels with the collection, as it is a many to many relationship, we must additionally call save_m2m() on the form object, elsewise the panels the user selected upon editing will not be associated with the collection
            form.save_m2m()
            form.save()
            messages.success(request, f"Dashboard '{edited_collection.title}' was successfully updated!")
            return redirect('user_collections')

    context['form'] = form 
    context['collections'] = collections
    return render(request, 'pages/collections.html',context)   


def show_collection(request, collection_id):
    """this is called by URL linked from several pages which display collection representations in rows.  returns and renders a template which presents a simple detailed view of collection, its identifying details, and its panels"""
    collection = PanelsCollection.objects.get(id=collection_id)
    context = {}
    context['collection'] = collection 
    panels = collection.panels.all()
    context['panels'] = panels
    return render(request, 'pages/show_collection.html', context)