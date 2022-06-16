"""marketplace_app.order URL Configuration
"""
from django.urls import path

from order import views


app_name = "order"

order_forms = getattr(views.OrderView, "order_forms", list())

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/<int:pk>", views.AddToCartView.as_view(), name="add_to_cart"),
    path(
        "cart/remove/<int:pk>",
        views.RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path("order/<int:pk>/", views.OrderDetail.as_view(), name="order_detail"),
    path(
        "order/",
        views.OrderView.as_view(order_forms),
        name="order",
    ),
    path("order/<int:pk>/payment/", views.PaymentView.as_view(), name="payment"),
]

