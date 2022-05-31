from django.urls import path

from .views import ContactsView, ShopDetailView, ShopListView


app_name = 'shop'

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts_detail'),
    path('shops/', ShopListView.as_view(), name='list'),
    path('shops/<int:pk>/', ShopDetailView.as_view(), name='detail'),
]
