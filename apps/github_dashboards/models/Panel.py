from django.db import models
from apps.accounts.models import User
from django.conf import settings
from django.utils import timezone
from .models_mixins.PanelMixin import PanelMixin


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

class Panel(models.Model, PanelMixin):
   
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

    svg = models.TextField(blank=True, null=True, editable=False)

    def __str__(self):
       return PanelMixin.__str__(self)
       

    def clean(self):
       PanelMixin.clean(self)


    def update(self):
       PanelMixin.save(self)