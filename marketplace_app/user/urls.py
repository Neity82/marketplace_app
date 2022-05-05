"""marketplace_app.user URL Configuration
"""
from django.urls import path

from user.views import UserAccount, UserProfile, HistoryOrders, HistoryViews, CompareProduct

app_name = 'user'

urlpatterns = [
    path('user/<int:pk>/account/', UserAccount.as_view(), name='user_account'),
    path('user/<int:pk>/profile/', UserProfile.as_view(), name='user_profile'),
    path('user/<int:pk>/orders/', HistoryOrders.as_view(), name='user_orders_list'),
    path('user/<int:pk>/views/', HistoryViews.as_view(), name='user_views'),
    path('compare/', CompareProduct.as_view(), name='compare_list'),

]
