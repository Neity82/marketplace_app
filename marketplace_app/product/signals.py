from django.dispatch import receiver, Signal

from user.models import UserProductView

product_view = Signal()


@receiver(product_view)
def add_product_view(**kwargs):
    UserProductView.add_object(
        user=kwargs["user"],
        product=kwargs["product"]
    )
