from django.urls import path
from django.contrib import admin
from django.urls import path, re_path
from apps.github_dashboards import views

urlpatterns = [
    # CRUD views for ReadingLists
    #path('', views.homepage, name="home"),
    path('details/<int:dash_id>/', views.panel_details, name='panel_details'),
    path('panels/<int:user_id>/', views.user_panels, name='user_panels'),
    path('dashboards/<int:user_id>/', views.panel_collections, name='panel_collections'),
    path('panels/', views.user_panels, name='user_panels'),
    path('dashboards/', views.panel_collections, name='panel_collections'),
    # path('list/delete/<int:list_id>/', views.reading_list_delete),
    # path('list/<int:list_id>/', views.reading_list_details),

    # # CRUD views for editing Books within ReadingLists
    # path('book-create/<int:list_id>/', views.create_book),
    # path('book-delete/<int:book_id>/', views.delete_book),

    # # CRUD views for voting on ReadingLists
    # path('list/<int:list_id>/vote/up/', views.reading_list_vote_up),
    # path('list/<int:list_id>/vote/down/', views.reading_list_vote_down),
]
