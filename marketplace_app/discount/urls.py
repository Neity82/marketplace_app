"""marketplace_app.discount URL Configuration
"""
from django.urls import path
from discount.views import SalesListView

app_name = "discount"

urlpatterns = [
    path("sales/", SalesListView.as_view(), name="list"),
]
