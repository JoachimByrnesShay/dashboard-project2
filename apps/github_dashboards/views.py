"""imports of libraries, functions, and modules needed for views.py"""
from django.shortcuts import render
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib import auth
"""from modules/*, custom modules containing utility fnctions and form classes"""
from .modules import custom_utils
from .models import DashboardPanel, PanelCollection
#from .modules import custom_forms

"""load any needed env variables"""
load_dotenv()


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

def panel_details(request):
    context = {}
    