from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DashboardPanel, PanelCollection
from django.utils.safestring import mark_safe


class DashboardPanelAdmin(admin.ModelAdmin):
    list_display = ["id", "creator", "github_username", "repo_name", "description", "panel_style", "panel_type", 'panel_size', "created", "modified"]
    list_display_links = ["github_username", "repo_name"]
    ordering = ('id',)
   

class PanelCollectionAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ["creator", "title", "description", "get_panels", "created", "modified"]
    list_display_links = ["title", "description"]

    
admin.site.register(PanelCollection, PanelCollectionAdmin)
admin.site.register(DashboardPanel, DashboardPanelAdmin)
