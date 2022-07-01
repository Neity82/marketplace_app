from django.dispatch import receiver, Signal

from user.models import UserProductView

get_product_detail_view = Signal()


@receiver(get_product_detail_view)
def add_product_view(**kwargs):
    UserProductView.add_object(
        user=kwargs["user"],
        product=kwargs["product"]
    )
