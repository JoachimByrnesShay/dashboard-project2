from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),

    path('view/', views.user_myaccount, name='user_myaccount'),
    path('edit/', views.user_edit, name='user_edit'),
    path('save/', views.user_save, name='user_save'),
    path('change_password/', views.user_change_password, name='user_change_password'),

    path('users/', views.users_view_all, name='users_view_all'),
    path('user/<user_id>', views.user_peer, name='user_peer'),
 ]
