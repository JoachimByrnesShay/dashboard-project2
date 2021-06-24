from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Panel, PanelsCollection



""" modeladmin class for panel """
class PanelAdmin(admin.ModelAdmin):
    # in case of tables, repo_name and panel_style will be empty/null.  use empty_value_display to customize appearance of empty values in admin panel
    empty_value_display = '-----------'
    # define fields to display at admin/github_dashboards/panel/""
    list_display = ["id", "creator", "github_username", "repo_name", "description", "panel_style", "panel_type", 'panel_size', "created", "modified"]
    # only this field is a link for the individual panel, links to admin/github_dashboards/panel/{panel.id}/change/""
    list_display_links = ["github_username"]
    # order display of panel data by id
    ordering = ('id',)

    #instantiate editable_objs as empty list.  this list is utilized in get_readonly_fields and get_queryset below
    editable_objs = [] 

    # for admin display, adds repo_name and panel_style to readonly_fields if instance is not found in editable_objs.  editable_objs will be all panels which are not table type.
    def get_readonly_fields(self, request, obj=None):
        if obj not in self.editable_objs:
            return self.readonly_fields + ('repo_name','panel_style',)
        return self.readonly_fields

    # overrides get_queryset method, sets self.editable_objs to be only those panel objects which are not 'TableOfRepos'.  i.e., only includes PyGal chart type panels.
    def get_queryset(self, request):
        self.editable_objs = Panel.objects.exclude(panel_type='TableOfRepos')
        return super(PanelAdmin, self).get_queryset(request)


    # if admin user uses admin panel to change a non-table to a table, sets repo_name and panel_style to null in that case
    def save_model(self, request, obj, form, change):
        if obj.panel_type == 'TableOfRepos':
            obj.repo_name = ''
            obj.panel_style = ''
        obj.save()
    

# modeladmin class for panelscollection
class PanelsCollectionAdmin(admin.ModelAdmin):
    # string_of_panels is not a model field but is a panelscollection instance method which returns <br> separated html text 
    # with each line a {github_username}/, + {repo_name} except for tables, with truncation to 10 chars for username, renders this as a field in admin display for each panelscollection
    list_display = ["creator", "title", "description", "string_of_panels", "created", "modified"]
    # only 'title' field is a link to edit individual panelscollection
    list_display_links = ["title"]

    
admin.site.register(Panel, PanelAdmin)
admin.site.register(PanelsCollection, PanelsCollectionAdmin)