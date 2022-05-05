"""marketplace_app.user URL Configuration
"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from user.views import UserAccount, UserProfile, HistoryViews, HistoryOrders, CustomLoginView, SignUpView

app_name = 'user'

urlpatterns = [
    path('user/<int:pk>/account/', UserAccount.as_view(), name='user_account'),
    path('user/<int:pk>/profile/', UserProfile.as_view(), name='user_profile'),
    path('user/<int:pk>/orders/', HistoryOrders.as_view(), name='user_orders_list'),
    path('user/<int:pk>/views/', HistoryViews.as_view(), name='user_views'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

]
