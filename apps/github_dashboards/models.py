from django.db import models
from apps.accounts.models import User
from .modules import custom_utils
# Create your models here.
from django.conf import settings
from django.utils import timezone
from pygal.style import *
from pygal import Bar, Pie, HorizontalBar, Gauge, Dot, Treemap
import sys
from django.utils.safestring import mark_safe

# class TimeStamped(models.Model):
#     creation_date = models.DateTimeField(editable=False)
#     last_modified = models.DateTimeField(editable=False)

#     def save(self, *args, **kwargs):
#         if not self.creation_date:
#             self.creation_date = timezone.now()

#         self.last_modified = timezone.now()
#         return super(TimeStamped, self).save(*args, **kwargs)

#     class Meta:
#         abstract = True


class PanelTypes(models.TextChoices):
    PIE= 'Pie', 'pie chart'
    BAR= 'Bar', 'bar chart'
    HORIZONTALBAR = 'HorizontalBar', 'horizontal bar chart'
    GAUGE = 'Gauge', 'gauge chart'
    DOT = "Dot", 'dot chart'
    TREEMAP = "Treemap", 'treemap chart'


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
    repo_description = models.TextField(null=True, blank=True)
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

        # print(list(repo))
        #return custom_utils.get_repo_languages_piechart(repo)
        #chart = get_chart_type(self.panel_type)
        chart = custom_utils.get_repo_languages_piechart(repo, chart_type, piechart_style)
        #print(chart)
        return chart

    def repo_get(self):
        repo = custom_utils.get_repo(self.github_username, self.repo_name)
        return repo

    def __str__(self):
        return self.github_username + '/' + self.repo_name
   

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
       # return "\n".join([a.visitor_name for a in obj.visitor_set.all()])
    #from django.utils.html import mark_safeget_panels.allow_tags = True
       