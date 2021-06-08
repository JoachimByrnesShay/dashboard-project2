from django.urls import path

from apps.github_dashboards import views

urlpatterns = [
    # CRUD views for ReadingLists
    # path('', views.homepage, name="home"),
    # path('list/create/', views.reading_list_create),
    # path('list/delete/<int:list_id>/', views.reading_list_delete),
    # path('list/<int:list_id>/', views.reading_list_details),

    # # CRUD views for editing Books within ReadingLists
    # path('book-create/<int:list_id>/', views.create_book),
    # path('book-delete/<int:book_id>/', views.delete_book),

    # # CRUD views for voting on ReadingLists
    # path('list/<int:list_id>/vote/up/', views.reading_list_vote_up),
    # path('list/<int:list_id>/vote/down/', views.reading_list_vote_down),
]
