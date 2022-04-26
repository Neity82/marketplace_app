"""marketplace_app.user URL Configuration
"""
from django.urls import path

from user.views import UserAccount, UserProfile, user_orders, user_views

app_name = 'user'

urlpatterns = [
    path('user/<int:pk>/account/', UserAccount.as_view(), name='user_account'),
    path('user/<int:pk>/profile/', UserProfile.as_view(), name='user_profile'),
    path('user/<int:pk>/orders/', user_orders, name='user_orders_list'),
    path('user/<int:pk>/views/', user_views, name='user_views'),

]
