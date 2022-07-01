import datetime

from marketplace_app.celery import app
from product.models import DailyOffer, Product


@app.task
def add_daily_offer():
    daily_offer_list = DailyOffer.objects.filter(
        select_date=datetime.datetime.today()
    )
    if daily_offer_list.exists() is False:
        product_day = Product.objects.filter(
            is_limited=True
        ).order_by("?").first()
        daily_offer = DailyOffer(product=product_day)
        daily_offer.save()


