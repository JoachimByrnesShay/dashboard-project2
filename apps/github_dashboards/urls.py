from django.urls import path
from django.contrib import admin
from django.urls import path, re_path
from apps.github_dashboards import views

urlpatterns = [
    path('details/<int:dash_id>/', views.panel_details, name='panel_details'),
    path('panels/<int:user_id>/', views.user_panels, name='user_panels'),
    path('dashboards/<int:user_id>/', views.panel_collections, name='panel_collections'),
    path('panels/', views.user_panels, name='user_panels'),
    path('edit_panel/<int:panel_id>/', views.edit_panel, name='edit_panel'), 
    path('dashboards/', views.panel_collections, name='panel_collections'),
    path('delete_panel/<int:panel_id>/', views.delete_panel, name='delete_panel'),
    path('delete_dashboard/<int:dashboard_id>/', views.delete_dashboard, name='delete_dashboard'),
    #path('table/', views.table, name='view_table'),
]