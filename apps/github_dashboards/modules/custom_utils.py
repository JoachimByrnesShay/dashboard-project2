""" imports of libraries and modules required for functions in this file (modules/custom_utils.py), which is imported into views.py"""
import os, sys, requests, pygal
from github import Github
from pygal.style import *
from .custom_forms import BlankGetRepoForm
from pygal import Bar, Pie, HorizontalBar, Gauge, Dot, Treemap


"""get all github repos via api for single user. default value for username
this is the only usecase for the current version of the app"""
def get_repos(username='JoachimByrnesShay'):
    url = "https://api.github.com/users/{username}/repos"
    token = os.getenv('GH_ACCESS_TOKEN')
    #print('token is here')
    #print(token)
    g = Github(token)
   
    user = g.get_user()
    login = user.login
   
    return user.get_repos()


def get_repo(user,repo):
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
    user = g.get_user(user)
    repo = user.get_repo(repo)
    return repo
"""params are a singular repo object and a repo field attribute as a string
   use getattr function to obtain repo.attribute value 
   prepare for sorting value and avoiding ASCII issues by using Lower() if value is not an int"""
def sortby_data(repo, sortby_value):
    item = getattr(repo, sortby_value)

    try:
        type(item) is int
        return item
    except:
        return item.lower()


"""get default repos and return svg barchart created via pygal using size attribute for repos"""
def get_repos_size_barchart():
    line_chart = pygal.Bar()
    line_chart.title = 'Repos by size'
    repos = get_repos()

    for repo in repos:
        line_chart.add(repo.name, repo.size)

    return line_chart.render_data_uri()


"""param is a single repo object. returns an svg pichart created via pygal using languages data from repo.languages_url (convered to json object)"""
def get_repo_languages_piechart(repo, panel_type, piechart_style):
    access_token = os.getenv('GH_ACCESS_TOKEN')
    headers = {'Authorization':"Token "+access_token}
    this_style = getattr(sys.modules[__name__], piechart_style) 
 
    #pie_chart = getattr(sys.modules[__name__], panel_type)(style=this_style)
    #pie_chart = pygal.Pie(style=this_style)
    pie_chart = getattr(sys.modules[__name__], panel_type)(style=this_style)
    pie_chart.title = "Languages used in this repository"
    print(repo)
    languages = requests.get(repo.languages_url, headers).json()
    #languages = requests.get(repo['languages_url'], headers).json()
    print('the repo is this one')
    
    for lang in languages:
        size = languages[lang]
        pie_chart.add(lang, size)
 
    pie = pie_chart.render_data_uri()
    return pie


"""check if requested user exists as a github public repo user, return None if not"""
def user_exists(user):
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)

    try:

        user = g.get_user(user)
    except:
        user = None
    
    return user


"""sets initial values as needed when new pichart form must be created after failed POST request 
if the user is valid, the initial form data will retain the user_name submitted va POST and a specialized plaeholder value will appear in repo_name field.
otherwise specialized placeholder values will appear both fields.  Placeholder content is set inside the BlankGetRepoForm class in custom_forms """
def nonexistent_repo_piechart_form(user_name, repo_name):
    initial = {}
    
    if user_exists(user_name):
        initial['user_name'] = user_name
    return BlankGetRepoForm(initial=initial)