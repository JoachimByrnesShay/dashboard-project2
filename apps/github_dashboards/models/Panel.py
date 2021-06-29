from django.db import models
from apps.accounts.models import User
from .models_mixins.PanelMixin import PanelMixin


class PanelTypes(models.TextChoices):
    """use TextChoices to delineate available options for panel types """
    TABLE='TableOfRepos', 'table- ALL repos for user'
    PIE= 'Pie', "pie chart- 1 repo"
    BAR= 'Bar', 'bar chart- 1 repo'
    HORIZONTALBAR = 'HorizontalBar', 'horizontal bar chart- 1 repo'
    GAUGE = 'Gauge', 'gauge chart- 1 repo'
    DOT = "Dot", 'dot chart- 1 repo'
    TREEMAP = "Treemap", 'treemap chart- 1 repo'


class PanelSizes(models.TextChoices):
    """ use TextChoices to deliniate avaialble options for panel sizes """
    SMALL = 'S', 'small'
    MEDIUM = 'M', 'medium'
    LARGE = 'L', "large"


class Panel(models.Model, PanelMixin):
    """ general class for all panels (including pygal charts and non-pygal tables).  mixes in PanelMixin, which is a custom class to organize methods which are mixed in to Panel as Panel instance methods"""
   
    # styletypes are styles available in pygal.styles. they are a simpler textchoices case, with no difference between database field value and display value necessary 
    StyleTypes = models.TextChoices('StyleType', "DefaultStyle DarkSolarizedStyle LightSolarizedStyle LightStyle CleanStyle \
    RedBlueStyle DarkColorizedStyle LightColorizedStyle TurquoiseStyle LightGreenStyle DarkGreenStyle DarkGreenBlueStyle BlueStyle")

    # one to many relationship user/creator (1) and panels (many)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # panel type choices are delineated in above PanelTypes class, default paneltype is designated 
    panel_type = models.CharField(
        max_length = 100,
        choices=PanelTypes.choices,
        default="Bar"
    )
    
    # github_username is required for all panels
    github_username = models.CharField(max_length=100)

    #github repo_name will not be required or used for tables, and will be blank in that case.
    repo_name = models.CharField(max_length=100, blank=True, null=True)

    #description is required
    description = models.TextField()

    #panel style choices are used for pygal charts
    panel_style = models.CharField(
        max_length=40,
        choices=StyleTypes.choices,
        default="DefaultStyle",
        null = True,
        blank = False,
    )
   
    # all panels including tables as well as pygal charts will be given a size based upon PanelSizes choices. The panel size value utilized to dynamically affect size of html element on display
    panel_size = models.CharField(
        max_length=20,
        choices=PanelSizes.choices,
        default="S"
    )

    # all panels will auto add created and modified fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # tables will not have svg so this field is not required.  Logic which handles svg presence/absence is found in models.models_mixins.PanelMixin.py
    svg = models.TextField(blank=True, null=True, editable=False)

    # __str__ calls __str__ as defined in  models.models_mixins.PanelMixin.py
    def __str__(self):
       return PanelMixin.__str__(self)
       
    # clean() is defined in models.models_mixins.PanelMixin.py to be consistent with organization of panel model methods which may be expected to be refactored or altered. 
    def clean(self):
       PanelMixin.clean(self)


       