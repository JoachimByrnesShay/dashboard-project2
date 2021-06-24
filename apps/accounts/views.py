
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import UserEditForm, RegisterForm


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from apps.github_dashboards.models import PanelsCollection, Panel
from apps.accounts.models import User

""" get all users for iterative display of username and a link (to a basic info page per user) for each in template"""
def users_view_all(request):
    users = User.objects.all()
    context = {
        'users':users,
        'users_active': 'active', 
    }
    return render(request, 'users.html', context)


"""get logged-in user instance for display in user's myaccount info page"""
@login_required
def user_myaccount(request):
    user = User.objects.get(id=request.user.id)
    count_dashboards = PanelsCollection.objects.filter(creator=request.user).count()
    count_panels = Panel.objects.filter(creator=request.user).count()
    context = {
        'user': user,
        'count_panels': count_panels,
        'count_dashboards': count_dashboards,
    }
    return render(request,'myaccount.html', context)
    
"""get selected peer user (any user) for rendering basic info about any user in template. choice made for log-in not required to see fundamental info about peer users"""
def user_peer(request, user_id):

    user = User.objects.get(id=user_id)
    dashboards = PanelsCollection.objects.filter(creator=user)
    panels = Panel.objects.filter(creator=user)
    context = {'other_user': user, 'panels': panels, 'dashboards': dashboards}
    return render(request, 'user_peer.html', context)

"""user_edit url is linked from myaccount.html and is utilized to populate user_edit form for logged-in-user."""
@login_required
def user_edit(request):
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


"""user_save url is linked from myaccount.html and is utilized to save user_edit form for logged-in user"""
@login_required
def user_save(request):
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

"""logged-in user change of password, called only from link on user myaccount page/template """
@login_required
def user_change_password(request):
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

"""anonymous user register new account"""
def user_register(request):
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

""" simple user logout"""
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "See you soon!  You are now logged out!")
    return redirect('home')

""" user login, if a @login_required view/url is called from link in template, login will redirect to the referring page, rather than home; otherise redirects to home"""
def user_login(request):
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

