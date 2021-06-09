from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import DashboardPanel





class DashboardPanelAdmin(admin.ModelAdmin):
    list_display = ["creator", "github_username", "repo_name", "repo_description", "panel_style", "panel_type"]
    list_display_links = ["creator", "github_username", "repo_name", "repo_description", "panel_style", "panel_type"]
admin.site.register(DashboardPanel, DashboardPanelAdmin)