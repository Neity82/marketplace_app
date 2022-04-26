from django.urls import path

from .views import ShopDetailView


app_name = 'shop'
urlpatterns = [
    path('shops/<int:pk>', ShopDetailView.as_view(), name='detail')
]
