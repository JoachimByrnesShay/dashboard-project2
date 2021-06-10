from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import DashboardPanel, PanelCollection
from django.utils.safestring import mark_safe




class DashboardPanelAdmin(admin.ModelAdmin):
    


    list_display = ["id", "creator", "github_username", "repo_name", "repo_description", "panel_style", "panel_type", "created", "modified"]
    list_display_links = ["github_username", "repo_name"]
    ordering = ('id',)
   

admin.site.register(DashboardPanel, DashboardPanelAdmin)


class PanelCollectionAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
   
    
    list_display = ["creator", "title", "description", "get_panels", "created", "modified"]
    list_display_links = ["title", "description"]

    

admin.site.register(PanelCollection, PanelCollectionAdmin)
