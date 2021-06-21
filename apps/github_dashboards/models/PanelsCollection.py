from django.db import models
from apps.accounts.models import User
from django.utils.safestring import mark_safe
from . import Panel

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