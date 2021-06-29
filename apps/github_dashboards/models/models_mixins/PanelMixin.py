import sys,os
from django.core.validators import ValidationError
from github import Github
from apps.github_dashboards.modules import custom_utils


""" panelmixin class contains custom methods for Panel class, for code organization purposes.  is "mixed-in" to Panel model in Panel.py.  thereby these are called as instance methods of Panel."""   
class PanelMixin:
    # utility to determine if panel instance is_table.  Utilized in conditional logic in templates
    def is_table(self):
        return self.panel_type == 'TableOfRepos'


    # utility to obtain a table's repos (for github user's account), for iteration inside of template as "for repo in repos".  only applies for table panels and not to pygal chart panels
    def get_repos(self):
        if self.is_table():
            return custom_utils.get_repos(self.github_username)
        else:
            return None

    
    def get_chart(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        piechart_style = self.panel_style
        chart_type= self.panel_type
        chart = custom_utils.get_repo_languages_chart(repo, chart_type, piechart_style)
        return chart


    # utilized in panel clean() override.  clean() will call this method to raise validation errors of github user does not exist or repo does not exist upon panel creation or update
    def clean_repo_name(self):
        token = os.getenv('GH_ACCESS_TOKEN')        
        g = Github(token)
        
        try:
            user = g.get_user(self.github_username)
        except:
             raise ValidationError('User does not exist on github')
      
        if self.panel_type != 'TableOfRepos':
            try:
                repo = user.get_repo(self.repo_name)
            except:
                raise ValidationError('Repo does not exist on github') 
        

    # utilized in panel clean() override.  clean() will call this method to create svg by calling get_chart() if panel is not a table (i.e. one true when there is a valid repo_name).   Otherwise svg is empty string.
    def clean_svg(self):
        if self.panel_type != 'TableOfRepos':
            self.svg = self.get_chart()
        else:
            self.svg = ''


    def clean_panel_style(self):
        if self.panel_type == 'TableOfRepos':
            self.panel_style = ''


    # string representation of instance will be username/ if instance is a table (in all cases where this is true, there is no repo_name), and otherwise as gihub_username/repo_name/
    def __str__(self):
        if self.panel_type == 'TableOfRepos':
            return self.github_username + '/'
        else:
            return self.github_username + '/' + self.repo_name
             
 
    # override of clean method, calling the above utility sub-clean methods in succession
    def clean(self):
         # without try,exception logic in clean_svg, clean_repo_name must be called before clean_svg
        self.clean_repo_name()
        self.clean_svg()
        self.clean_panel_style()

