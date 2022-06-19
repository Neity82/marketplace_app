"""marketplace_app.order URL Configuration
"""
from django.urls import path

from order import views


app_name = "order"

order_forms = getattr(views.OrderView, "order_forms", list())

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/<int:pk>", views.AddToCartView.as_view(), name="add-to-cart"),
    path("cart/add/<int:pk>/<int:cnt>", views.AddToCartView.as_view(), name="add-to-cart-cnt"),
    path("cart/add/<int:pk>/shop/<int:shop_id>",
         views.AddToCartView.as_view(), name="add-to-cart-shop"),
    path(
        "cart/remove/<int:pk>",
        views.RemoveFromCartView.as_view(),
        name="remove-from-cart",
    ),
    path("order/<int:pk>/", views.OrderDetail.as_view(), name="order-detail"),
    path(
        "order/",
        views.OrderView.as_view(order_forms),
        name="order",
    ),
    path("order/<int:pk>/payment/", views.PaymentView.as_view(), name="payment"),
]
