from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Panel, PanelsCollection
from django.utils.safestring import mark_safe


# class PanelAdmin(admin.ModelAdmin):
#     list_display = ["id", "creator", "github_username", "repo_name", "description", "panel_style", "panel_type", 'panel_size', "created", "modified"]
#     list_display_links = ["github_username"]

#     ordering = ('id',)
#     # def has_add_permission(self, request, obj=None):
#     #     return False
#     last = False
#     def get_form(self, request, obj=None,**kwargs):
#         form = super(PanelAdmin, self).get_form(request, obj, **kwargs)
#         #super(PanelAdmin,self).__init__(request,*args, **kwargs)
#         print(obj)
#         if form.base_fields.get('repo_name') == 'TableOfRepos':
#             print('yes')
#             last = True
#         else:
#             print('no')
#             last = False
#         #if form.base_fields['panel_type'] == "TableOfRepos":
#         #   last = True 
#         return form

    # def has_change_permission(self, request, obj=None):
    #     return False
class PanelAdmin(admin.ModelAdmin):
    list_display = ["id", "creator", "github_username", "repo_name", "description", "panel_style", "panel_type", 'panel_size', "created", "modified"]
    #fields = ["creator", "github_username", "repo_name", "description", "panel_style", "panel_type", 'panel_size']
    list_display_links = ["github_username"]
    editable_objs = [] 

    ordering = ('id',)
    # def has_change_permission(self, request, obj=None):
    #     #return obj is None or obj.owner == request.user
    #     return obj in self.editable_objs
    def get_readonly_fields(self, request, obj=None):
        if obj not in self.editable_objs:
            return self.readonly_fields + ('repo_name','panel_style',)
        return self.readonly_fields
    # def not_edit(self, request, obj=None):
    #     if obj not in self.editable_objs:
    #         form = super(PanelAdmin, self).get_form(request, obj, **kwargs)
    #         form.base_fields['repo_name'].readonly= True 

    def get_queryset(self, request):
        # Stores all the BankAccount instances that the logged in user is owner of
        self.editable_objs = Panel.objects.exclude(panel_type='TableOfRepos')
        return super(PanelAdmin, self).get_queryset(request)


    def save_model(self, request, obj, form, change):
        if obj.panel_type == 'TableOfRepos':
            obj.repo_name = ''
            obj.panel_style = ''
        obj.save()
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(PanelAdmin, self).get_form(request, obj=obj, **kwargs)
    #     if form.base_fields['panel_type'] == "TableOfRepos":
    #         d
            
    #     return form

# def get_form(self, request, obj=None, **kwargs):
#     if request.user.is_superuser:   
#         return EmployerSuperUserForm
#     else:
#         return EmployerForm
#         self.fields=['employer_verified']
#     def __init__(self):
#         form = super(PanelAdmin, self).get_form(request, obj, **kwargs)
#         i
            
    # def get_readonly_fields(self, request, obj=None):
    #     if self.obj.pk:
    #         return ['description', 'city_code', 'customer']
    #     else:
    #         return []
    # def get_form(self, request, obj=None, **kwargs):
        
        
    #     #elf.data = self.data.copy()
    #     #cleaned_data = super(PanelForm, self).clean()
    #       #     self.exclude('repo_name',)
    #     form = super(PanelAdmin, self).get_form(request, obj, **kwargs)
    #    #if obj.objects.filter("panel_type"=="TableOfRepos"):
    #     if form.base_fields['panel_type'] == "TableOfRepos":
    #         model = Step
    #    exclude = ['parent']
    #    readonly_fields=('parent', )
    #     #     self.exclude('panel_type',)
     
    #     # return form
    #         form.base_fields['repo_name'] = None
    #         form.base_fields['panel_style'].value = None
    #         form.base_fields['panel_style'].widget.initial_value = "something"
    #     # #     form.base_fields['repo_name'].disabled = True
    #     # # #     # this will hide the null option for the parent field
    #     # #     #form.base_fields["repo_name"].widget.attrs['readonly'] = True
    #     # #     form.base_fields['repo_name'].widget.attrs['disabled'] = 'disabled'
    #     # #     #form.base_fields["panel_style"].widget.attrs['readonly'] = True
    #     # #     form.base_fields['panel_style'].widget.attrs['disabled'] = True
    #     # #field = form.base_fields["your_foreign_key_field"]
    #     #     field1.widget.can_add_related = False
    #     #     field1.widget.can_change_related = False
    #     #     field1.widget.can_delete_related = False
    #     #     field2.widget.can_add_related = False
    #     #     field2.widget.can_change_related = False
    #     #     field2.widget.can_delete_related = False
    #     # return form

    #     return form
    # def formfield_for_repo_name(self, *args, **kwargs):
    #     formfield = super().formfield_for_repo_name(*args, **kwargs)

    #     formfield.widget.can_delete_related = False
    #     formfield.widget.can_change_related = False
    #     # formfield.widget.can_add_related = False  # can change this, too
    #     # formfield.widget.can_view_related = False  # can change this, too

    #     return formfield

class PanelsCollectionAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
  
    list_display = ["creator", "title", "description", "string_of_panels", "created", "modified"]
    list_display_links = ["title", "description"]

    

admin.site.register(Panel, PanelAdmin)
admin.site.register(PanelsCollection, PanelsCollectionAdmin)