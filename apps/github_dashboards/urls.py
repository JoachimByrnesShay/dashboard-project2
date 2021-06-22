from django.urls import path
from django.contrib import admin
from django.urls import path, re_path
from apps.github_dashboards import views

urlpatterns = [
    path('details/<int:dash_id>/', views.panel_details, name='panel_details'),
    path('panels/<int:user_id>/', views.user_panels, name='user_panels'),
    path('collections/<int:user_id>/', views.panel_collections, name='panel_collections'),
    path('panels/', views.user_panels, name='user_panels'),
    path('edit_panel/<int:panel_id>/', views.edit_panel, name='edit_panel'), 
    path('edit_collection/<int:collection_id>/', views.edit_collection, name='edit_collection'),
    path('collections/', views.panel_collections, name='panel_collections'),
    path('delete_panel/<int:panel_id>/', views.delete_panel, name='delete_panel'),
    path('delete_collection/<int:collection_id>/', views.delete_collection, name='delete_collection'),
    #path('table/', views.table, name='view_table'),
]