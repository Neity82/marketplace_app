import random

from celery.schedules import crontab
from marketplace_app.celery import app
from order.models import Order
from payments.models import Payment


MESSAGES = {
    "error": [
        "Вам отключили SWIFT.",
        "Вы в санкционном списке США.",
    ],
    "success": "Оплата прошла успешно",
}


@app.task
def check_payments_statuses():
    payments = Payment.objects.filter(status="processing")

    if payments:
        for payment in payments:
            order = Order.objects.filter(payment=payment).first()
            acquirer_resp = random.randint(1, 5)

            if acquirer_resp in (3, 4):
                payment.status = "success"
                payment.message = MESSAGES["success"]
                order.state = "paid"
                order.save()

            if acquirer_resp == 5:
                payment.status = "error"
                payment.message = MESSAGES["error"][
                    random.randint(0, len(MESSAGES["error"]) - 1)
                ]

        Payment.objects.bulk_update(payments, fields=["status", "message"])
