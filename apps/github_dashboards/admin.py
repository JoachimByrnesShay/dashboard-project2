from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DashboardPanel, PanelCollection
from django.utils.safestring import mark_safe


class DashboardPanelAdmin(admin.ModelAdmin):
    list_display = ["id", "creator", "github_username", "repo_name", "description", "panel_style", "panel_type", 'panel_size', "created", "modified"]
    list_display_links = ["github_username", "repo_name"]
    ordering = ('id',)
   
    def get_form(self, request, obj=None, **kwargs):
        form = super(DashboardPanelAdmin, self).get_form(request, obj, **kwargs)

       #if obj.objects.filter("panel_type"=="TableOfRepos"):
        if form.fields['panel_type'] == "TableOfRepos":

            # this will hide the null option for the parent field
            form.fields["repo_name"].widget.attrs['readonly'] = True
            form.fields['repo_name'].widget.attrs['disabled'] = True

        return form
   

class PanelCollectionAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ["creator", "title", "description", "get_panels", "created", "modified"]
    list_display_links = ["title", "description"]

    
admin.site.register(PanelCollection, PanelCollectionAdmin)
admin.site.register(DashboardPanel, DashboardPanelAdmin)
