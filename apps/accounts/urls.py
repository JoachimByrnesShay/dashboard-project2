from django.urls import path

from apps.accounts import views

urlpatterns = [
    # path('login/', views.log_in, name='login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('users/', views.users_view_all, name='view_all_users'),
    path('myaccount/', views.user_myaccount, name='user_myaccount'),
    # path('users/<username>/', views.view_profile, name='view_profile'),
 ]
