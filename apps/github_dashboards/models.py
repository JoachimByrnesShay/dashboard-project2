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
from django.core.exceptions import ValidationError

class PanelTypes(models.TextChoices):
    TABLE='TableOfRepos', 'table- ALL repos for user'
    PIE= 'Pie', 'pie chart- 1 repo'
    BAR= 'Bar', 'bar chart- 1 repo'
    HORIZONTALBAR = 'HorizontalBar', 'horizontal bar chart- 1 repo'
    GAUGE = 'Gauge', 'gauge chart- 1 repo'
    DOT = "Dot", 'dot chart- 1 repo'
    TREEMAP = "Treemap", 'treemap chart- 1 repo'


class DashboardPanel(models.Model):
    PanelSizes = models.TextChoices('PanelType', "Small Medium Large")

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
    repo_name = models.CharField(max_length=100)
    description = models.TextField()
    # style_type = models.TextChoices('StyleType', "DefaultStyle DarkSolarizedStyle LightSolarizedStyle LightStyle CleanStyle \
    # RedBlueStyle DarkColorizedStyle LightColorizedStyle TurquoiseStyle LightGreenStyle DarkGreenStyle DarkGreenBlueStyle BlueStyle")
    panel_style = models.CharField(
        max_length=40,
        choices=StyleTypes.choices,
        default="DefaultStyle",
    )
   
    panel_size = models.CharField(
        max_length=20,
        choices=PanelSizes.choices,
        default="Medium"
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_chart(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        print("INSIDE GET CHART")
        print(repo)
       # piechart_style = getattr(sys.modules[__name__], self.panel_style)
        #piechart_style = getattr(sys.modules[__name__], self.panel_style)
        piechart_style = self.panel_style
        chart_type= self.panel_type

        chart = custom_utils.get_repo_languages_piechart(repo, chart_type, piechart_style)

        return chart

    svg = models.TextField(blank=True, null=True, editable=False)

    def repo_get(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        return repo

    def __str__(self):
        return self.github_username + '/' + self.repo_name
 

    

    def clean(self):
        token = os.getenv('GH_ACCESS_TOKEN')
        g = Github(token)
       
        try:
            user = g.get_user(self.github_username)
        except:
             raise ValidationError('User does not exist on github')
        # if repo:
        try:
            repo = user.get_repo(self.repo_name)
        except:
            raise ValidationError('Repo does not exist on github') 
        try:
            self.svg = self.get_chart()
        except:
            raise Exception('svg chart could not be built from this data')

class PanelCollection(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    panels=models.ManyToManyField(DashboardPanel)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def get_panels(self):
        return mark_safe("<br>".join([" %s.../%s" % (p.github_username[0:5],p.repo_name) for p in self.panels.all()]))
