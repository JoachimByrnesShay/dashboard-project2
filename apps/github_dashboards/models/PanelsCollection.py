from django.db import models
from django.utils.safestring import mark_safe
from apps.accounts.models import User
from . import Panel


class PanelsCollection(models.Model):
    """ panelscollection class is a class to contain multiple panels, using a many_to_many relationship between the collection and panels """

    # establish one to many relationship between user and panelscollection instance
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    panels=models.ManyToManyField(Panel)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def string_of_panels(self, truncate=True):
       """ returns a <br> separated list of the panels contained in the panelscollection, utilized as html text in admin display as well as templates"""
       
       self_panels = self.panels.all()

       # truthiness of truncate argument determines whether this method will return full repo usernames as part of the output, or truncated usernames.  slicing to None, i.e.[:None], intead of an index is valid syntax and is equivalent to [:] 
       if not truncate:
           end_slice = None
           ellipses = ''
       else:
           end_slice = 10
           ellipses = '...'
    
       # using list comprehension for each panel in self_panels, create formatted string of github_username (truncated depending on truncate argument)/ + empty string OR panel.repo_name if it exists.
       # join each resulting string per panel with "<br>" for usage in html (used in templates and in admin display). use mark_safe so <br> is not escaped
       
       return mark_safe("<br>".join([f"{panel.github_username[:end_slice]}{ellipses}/{panel.repo_name or ''}" for panel in self_panels]))
