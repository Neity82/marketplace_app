import random

from payments.models import Payment


MESSAGES = {
    "error": [
        "Вам отключили SWIFT.",
        "Вы в санкционном списке США.",
    ],
}


# TODO повесить декоратор celery shared_task
def check_payments_statuses():
    payments = Payment.objects.filter(status="processing")

    if payments:
        for payment in payments:
            acquirer_resp = random.randint(1, 5)

            if acquirer_resp in (3, 4):
                payment.status = "success"

            if acquirer_resp == 5:
                payment.status = "error"
                payment.message = MESSAGES["error"][random.randint(0, len(MESSAGES["error"]) - 1)]

        Payment.objects.bulk_update(payments, fields=["status", "message"])
