"""marketplace_app.user URL Configuration
"""
from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from user import views

app_name = "user"

urlpatterns = [
    path("user/<int:pk>/account/", views.UserAccount.as_view(), name="user_account"),
    path("user/<int:pk>/profile/", views.UserProfile.as_view(), name="user_profile"),
    path(
        "user/<int:pk>/orders/", views.HistoryOrders.as_view(), name="user_orders_list"
    ),
    path("user/<int:pk>/views/", views.HistoryViews.as_view(), name="user_views"),
    path(
        "compare/category/<int:pk>/",
        views.CompareProduct.as_view(),
        name="compare_list",
    ),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "password_reset/",
        views.PasswordResetViewCustom.as_view(),
        name="password_reset",
    ),
]
