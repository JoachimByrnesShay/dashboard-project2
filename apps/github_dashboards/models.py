from django.db import models
from apps.accounts.models import User
from .modules import custom_utils
# Create your models here.
from django.conf import settings
from django.utils import timezone
from pygal.style import *
from pygal import Bar, Pie, HorizontalBar, Gauge, Dot, Treemap
import sys, os
from django.utils.safestring import mark_safe
from github import Github
from django.core.validators import ValidationError

class PanelTypes(models.TextChoices):
    TABLE='TableOfRepos', 'table- ALL repos for user'
    PIE= 'Pie', "pie chart- 1 repo\n"
    BAR= 'Bar', 'bar chart- 1 repo'
    HORIZONTALBAR = 'HorizontalBar', 'horizontal bar chart- 1 repo'
    GAUGE = 'Gauge', 'gauge chart- 1 repo'
    DOT = "Dot", 'dot chart- 1 repo'
    TREEMAP = "Treemap", 'treemap chart- 1 repo'

class PanelSizes(models.TextChoices):
    SMALL = 'S', 'small'
    MEDIUM = 'M', 'medium'
    LARGE = 'L', "large"

class Panel(models.Model):
    

    StyleTypes = models.TextChoices('StyleType', "DefaultStyle DarkSolarizedStyle LightSolarizedStyle LightStyle CleanStyle \
    RedBlueStyle DarkColorizedStyle LightColorizedStyle TurquoiseStyle LightGreenStyle DarkGreenStyle DarkGreenBlueStyle BlueStyle")
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    #creator = UserForeignKey(auto_user=True, on_delete=models.CASCADE)
    panel_type = models.CharField(
        max_length = 100,
        choices=PanelTypes.choices,
        default="Bar"
    )
    
    github_username = models.CharField(max_length=100)
    repo_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    panel_style = models.CharField(
        max_length=40,
        choices=StyleTypes.choices,
        default="",
        null = True,
        blank = True,
    )
   
    panel_size = models.CharField(
        max_length=20,
        choices=PanelSizes.choices,
        default="S"
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_chart(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        print(repo.get_contents("README.md"))
        piechart_style = self.panel_style
        chart_type= self.panel_type
        chart = custom_utils.get_repo_languages_chart(repo, chart_type, piechart_style)
        print(chart)
        return chart

    svg = models.TextField(blank=True, null=True, editable=False)


    def __str__(self):
        if self.repo_name:
            return self.github_username + '/' + self.repo_name
        else:
            return self.github_username
 

    def clean_repo_name(self):
        token = os.getenv('GH_ACCESS_TOKEN')
        
        g = Github(token)
        print(g)
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
        if self.repo_name != 'TableOfRepos':
            self.svg = self.get_chart()
        else:
            self.svg = ''
       
    def clean(self):
        # without try,exception logic in clean_svg, clean_repo_name must be called before clean_svg
        self.clean_repo_name()
        self.clean_svg()
 

class PanelsCollection(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    panels=models.ManyToManyField(Panel)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def string_of_panels(self):
       import itertools

       #self_panels = set(panel for panel in self.panels.all())
       self_panels = self.panels.all()
        
       return mark_safe("<br>".join([f"{panel.github_username}.../{panel.repo_name}" for panel in self_panels]))