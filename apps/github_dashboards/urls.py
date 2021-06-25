from django.urls import path
from django.contrib import admin
from django.urls import path, re_path
from apps.github_dashboards import views

urlpatterns = [
    # show all panels or all collections for logged-in-user, the view function also provides add new panel or add new collection functionality.  rendered templates provide links to urls/views providing edit, delete, and show single panel/collection.
    path('panels/', views.user_panels, name='user_panels'),
    path('collections/', views.user_collections, name='user_collections'),

    # show single instance urls show individual panel or individual collection and its details in full page view
    path('show_panel/<int:panel_id>/', views.show_panel, name='show_panel'),
    path('show_collection/<int:collection_id>/', views.show_collection, name='show_collection'),
 
    # edit single panel and delete single collection urls are linked only from the templates rendered by 'user_panels' and 'user_collections'
    path('edit_panel/<int:panel_id>/', views.edit_panel, name='edit_panel'), 
    path('edit_collection/<int:collection_id>/', views.edit_collection, name='edit_collection'),
    path('delete_panel/<int:panel_id>/', views.delete_panel, name='delete_panel'),
    path('delete_collection/<int:collection_id>/', views.delete_collection, name='delete_collection'),
]