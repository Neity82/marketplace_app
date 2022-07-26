from django.db.models import Q
from django.views.generic import list
import datetime
from .models import Discount


class SalesListView(list.ListView):
    context_object_name = "sales"
    queryset = Discount.objects.filter(
        is_active=True,
    )
    template_name = "discount/sale.html"
    paginate_by = 12

    def get_queryset(self):
        today = datetime.datetime.today()
        queryset = (
            Discount.objects.filter(is_active=True)
            .filter(
                Q(start_at__lte=today) & (Q(finish_at__gte=today) | Q(finish_at=None))
            )
            .order_by("finish_at")
        )
        return queryset
