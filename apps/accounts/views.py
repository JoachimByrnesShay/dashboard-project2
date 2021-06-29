
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from apps.accounts.forms import UserEditForm, RegisterForm
from apps.github_dashboards.models import PanelsCollection, Panel
from apps.accounts.models import User


def users_view_all(request):
    """ get all users for iterative display of username and a link (to a basic info page per user) for each in template"""
    users = User.objects.all()
    context = {
        'users':users,
        'users_active': 'active', 
    }
    return render(request, 'users.html', context)


@login_required
def user_myaccount(request):
    """get logged-in user instance for display in user's myaccount info page"""
    user = User.objects.get(id=request.user.id)
    count_collections = PanelsCollection.objects.filter(creator=request.user).count()
    count_panels = Panel.objects.filter(creator=request.user).count()
    context = {
        'user': user,
        'count_panels': count_panels,
        'count_collections': count_collections,
    }
    return render(request,'myaccount.html', context)
    

def user_peer(request, user_id):
    """get selected peer user (any user) for rendering basic info about any user in template. choice made for log-in not required to see fundamental info about peer users"""
    user = User.objects.get(id=user_id)
    # another method for obtaining count of panels in collection.  use Count to annotate query, per https://stackoverflow.com/questions/5439901/getting-a-count-of-objects-in-a-queryset-in-django
    collections = PanelsCollection.objects.filter(creator=user).annotate(panel_count=Count('panels'))
    panels = Panel.objects.filter(creator=user)
    context = {'other_user': user, 'panels': panels, 'collections': collections}

    return render(request, 'user_peer.html', context)


@login_required
def user_edit(request):
    """user_edit url is linked from myaccount.html and is utilized to populate user_edit form for logged-in-user."""
    user = User.objects.get(id=request.user.id)
    count_dashboards = PanelsCollection.objects.filter(creator=request.user).count()
    count_panels = Panel.objects.filter(creator=request.user).count()
    form = UserEditForm(instance=user)

    if form.is_valid():
        form.save()

    print(form)
    context = {
        'user': user,
        'count_panels': count_panels,
        'count_dashboards': count_dashboards,
        'form':form,
    }
    return render(request, 'myaccount.html', context)


@login_required
def user_save(request):
    """user_save url is linked from myaccount.html and is utilized to save user_edit form for logged-in user"""
    if request.method == "POST":
        context = {}
        form = UserEditForm(request.POST, instance=request.user)
       
        print(request.POST)
           
        if form.is_valid():
            form.save()
            print(form.errors)
            return redirect('user_myaccount')
        else:
            print(form.errors)
            context['form'] = form
            return render(request, 'myaccount.html', context)


@login_required
def user_change_password(request):
    """logged-in user change of password, called only from link on user myaccount page/template """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  #
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_myaccount')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'form': form
    })


def user_register(request):
    """anonymous user register new account"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'Welcome! You are now registered!')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }       
    return render(request, 'register.html', context)


def user_login(request):
    """ user login, if a @login_required view/url is called from link in template, login will redirect to the referring page, rather than home; otherise redirects to home"""
    if request.GET:
        import re
        obj_name = re.sub("[\[\]\/]", '', str(request.GET['next']))
        messages.warning(request, f"LOGIN or SIGNUP to see your {obj_name.upper()}")

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())

            if messages:
                # clear messages iterator first, technique from imaurer at https://stackoverflow.com/questions/4083164/django-remove-message-before-they-are-displayed
                list(messages.get_messages(request))
            messages.success(request, "You are now logged in!")

            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


@login_required
def user_logout(request):
    """ simple user logout"""
    logout(request)
    messages.success(request, "See you soon!  You are now logged out!")
    return redirect('home')

