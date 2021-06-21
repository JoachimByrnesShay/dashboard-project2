

import sys, os
from django.core.validators import ValidationError
from github import Github
from apps.github_dashboards.modules import custom_utils



class PanelMixin:

    def get_chart(self):
       
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        piechart_style = self.panel_style
        chart_type= self.panel_type
        chart = custom_utils.get_repo_languages_chart(repo, chart_type, piechart_style)
        return chart


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
        

    def clean_svg(self):
        if self.repo_name:
            self.svg = self.get_chart()
        else:
            self.svg = ''

    
    def __str__(self):

        if self.repo_name:
            return self.github_username + '/' + self.repo_name
        else:
            return self.github_username
 

    def clean(self):
         # without try,exception logic in clean_svg, clean_repo_name must be called before clean_svg
        self.clean_repo_name()
        self.clean_svg()

    def save(self):
        self.clean_repo_name()
        self.clean_svg()
        return self
