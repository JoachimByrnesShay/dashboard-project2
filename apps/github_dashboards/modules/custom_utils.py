""" imports of libraries and modules required for functions in this file (modules/custom_utils.py), which is imported into views.py"""
import os, sys, requests, pygal
from github import Github
from pygal.style import *
from pygal import Bar, Pie, HorizontalBar, Gauge, Dot, Treemap

      
""" get and return all repos for github_username.  existence of githubusername and repos is all validated separately at point of panel creation """          
def get_repos(username):
    url = "https://api.github.com/users/{username}/repos"
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
   
    user = g.get_user()
    login = user.login
   
    return user.get_repos()

""" get individual github repo for username/reponame """
def get_repo(user,repo):
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
    user = g.get_user(user)
    repo = user.get_repo(repo)
    return repo


"""returns an svg pichart created via pygal using languages data from repo.languages_url (languages_url data converted to json object)"""
def get_repo_languages_chart(repo, panel_type, chart_style):
    access_token = os.getenv('GH_ACCESS_TOKEN')
    # preparing headers for github api access, because languages_url data will have to be obtained via requests and not pygithub
    headers = {'Authorization':"Token "+access_token}

    # chart_style is a string (panel object attribute). getattr will use the string name to convert it to a class instance of the same name (pygal styles are class objects)
    this_style = getattr(sys.modules[__name__], chart_style) 

    # same strategy with panel.panel_type, instantiate the chart using paneltype and selected style
    chart = getattr(sys.modules[__name__], panel_type)(style=this_style, width=400, height=200)
    chart.title = "Languages used in this repository"
 
    # repo.languages_url value is an actual url.  utilize requests to get the content at url via github api and convert content to json.
    languages = requests.get(repo.languages_url, headers).json()
 
    # the json keys are each language, and each value is "size" of language use in the repo per number of bytes in code
    for lang in languages:
        size = languages[lang]
        chart.add(lang, size)
 
    rendered_chart = chart.render_data_uri()
    return rendered_chart
