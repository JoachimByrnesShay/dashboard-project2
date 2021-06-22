""" imports of libraries and modules required for functions in this file (modules/custom_utils.py), which is imported into views.py"""
import os, sys, requests, pygal
from github import Github
from pygal.style import *

from pygal import Bar, Pie, HorizontalBar, Gauge, Dot, Treemap


"""get all github repos via api for single user. default value for username
this is the only usecase for the current version of the app"""
def clean_repo_name(self):
    token = os.getenv('GH_ACCESS_TOKEN')
    
    g = Github(token)
    
    try:
        user = g.get_user(self.github_username)
    except:
         raise ValidationError('User does not exist on github')
    # if repo:
  
    if self.panel_type != 'TableOfRepos':
        try:
            repo = user.get_repo(self.repo_name)
        except:
            raise ValidationError('Repo does not exist on github') 

                
def get_repos(username):
    url = "https://api.github.com/users/{username}/repos"
    token = os.getenv('GH_ACCESS_TOKEN')
    #print('token is here')
    #print(token)
    g = Github(token)
   
    user = g.get_user()
    login = user.login
   
    return user.get_repos()

def confirm_user_and_repo_exist(user,repo):
        token = os.getenv('GH_ACCESS_TOKEN')
        g = Github(token)
  
        user = g.get_user(user)
        repo = user.get_repo(repo)
        return repo


def get_repo(user,repo):
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
    print(g)
    user = g.get_user(user)
    print(g)
    repo = user.get_repo(repo)
    print(repo)
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




"""param is a single repo object. returns an svg pichart created via pygal using languages data from repo.languages_url (convered to json object)"""
def get_repo_languages_chart(repo, panel_type, chart_style):
    access_token = os.getenv('GH_ACCESS_TOKEN')
    headers = {'Authorization':"Token "+access_token}
    this_style = getattr(sys.modules[__name__], chart_style) 
 
    chart = getattr(sys.modules[__name__], panel_type)(style=this_style, width=400, height=200)
    chart.title = "Languages used in this repository"
 
    languages = requests.get(repo.languages_url, headers).json()
 
    for lang in languages:
        size = languages[lang]
        chart.add(lang, size)
 
    rendered_chart = chart.render_data_uri()
    return rendered_chart


"""check if requested user exists as a github public repo user, return None if not"""
def user_exists(user):
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)

    try:

        user = g.get_user(user)
    except:
        user = None
    
    return user


