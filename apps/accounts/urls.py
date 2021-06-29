from django.urls import path

from apps.accounts import views

urlpatterns = [
    # basic user account management urls
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),

    # enhanced user account management urls for viewing/editing/saving logged-in user account details
    path('view/', views.user_myaccount, name='user_myaccount'),
    path('edit/', views.user_edit, name='user_edit'),
    path('save/', views.user_save, name='user_save'),
    path('change_password/', views.user_change_password, name='user_change_password'),

    # public user urls, allowing a basic level of visibility of public peer user information to anonymous and logged-in users
    path('users/', views.users_view_all, name='users_view_all'),
    path('user/<user_id>', views.user_peer, name='user_peer'),
 ]
