from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logut/', views.logout_user, name='logout'),
    path('register-user/', views.register_user, name='register'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('account', views.user_account, name='account'),
    path('edit-account', views.edit_account, name='edit_account'),
    path('create-skill', views.create_skill, name='create_skill'),
    path('edit-skill/<str:pk>/', views.edit_skill, name='edit_skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='view_message'),
    path('create-message/<str:pk>/', views.create_message, name='create_message'),
]
