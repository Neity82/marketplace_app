from django.urls import path

from .views import ShopDetailView, ShopListView


app_name = 'shop'

urlpatterns = [
    path('shops/', ShopListView.as_view(), name='list'),
    path('shops/<int:pk>/', ShopDetailView.as_view(), name='detail')
]
