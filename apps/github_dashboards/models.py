from django.db import models
from apps.accounts.models import User
from .modules import custom_utils
# Create your models here.
from django.conf import settings
import sys


class PanelTypes(models.TextChoices):
    LANG_PIE= 'lang-pie', 'pie chart of languages used'
    LANG_BAR= 'lang-bar', 'bar chart of languages used'



class DashboardPanel(models.Model):
    StyleTypes = models.TextChoices('StyleType', "DefaultStyle DarkSolarizedStyle LightSolarizedStyle LightStyle CleanStyle \
    RedBlueStyle DarkColorizedStyle LightColorizedStyle TurquoiseStyle LightGreenStyle DarkGreenStyle DarkGreenBlueStyle BlueStyle")
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    #creator = UserForeignKey(auto_user=True, on_delete=models.CASCADE)
     
    
    github_username = models.CharField(max_length=100)
    repo_name = models.CharField(max_length=100)
    repo_description = models.TextField(null=True, blank=True)
    # style_type = models.TextChoices('StyleType', "DefaultStyle DarkSolarizedStyle LightSolarizedStyle LightStyle CleanStyle \
    # RedBlueStyle DarkColorizedStyle LightColorizedStyle TurquoiseStyle LightGreenStyle DarkGreenStyle DarkGreenBlueStyle BlueStyle")
    panel_style = models.CharField(
        max_length=40,
        choices=StyleTypes.choices,
        default="DefaultStyle",
    )
    panel_type = models.CharField(
        max_length = 100,
        choices=PanelTypes.choices,
        default="lang-bar"
    )
    

    def get_chart(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        #print(repo)
       # piechart_style = getattr(sys.modules[__name__], self.panel_style)
        piechart_style = self.panel_style
        chart_type= self.panel_type
        # print(list(repo))
        #return custom_utils.get_repo_languages_piechart(repo)
        #chart = get_chart_type(self.panel_type)
        chart = custom_utils.get_repo_languages_piechart(repo, chart_type, piechart_style)
        #print(chart)
        return chart

    def repo_get(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        return repo
   

class PanelsCollection(models.Model):
    title = models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    panels=models.ManyToManyField(DashboardPanel)
