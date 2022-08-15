from django.core import mail
from django import forms
from django.utils.translation import ugettext_lazy

from marketplace_app.settings import DEBUG
from info.models import Settings


class FeedBackForm(forms.Form):
    """Форма обратной связи на странице контактов"""

    name = forms.CharField(
        min_length=5,
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "id": "name",
                "name": "name",
                "placeholder": ugettext_lazy("name"),
            }
        ),
    )

    email = forms.CharField(
        min_length=5,
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "id": "mail",
                "name": "mail",
                "placeholder": ugettext_lazy("e-mail"),
            }
        ),
    )

    site = forms.CharField(
        min_length=5,
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "id": "site",
                "name": "site",
                "placeholder": ugettext_lazy("website"),
            }
        ),
    )

    message = forms.CharField(
        min_length=5,
        max_length=500,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "id": "message",
                "name": "message",
                "placeholder": ugettext_lazy("message"),
            }
        ),
    )

    def send_email(self) -> None:
        """Метод отправки письма из формы обратной связи"""
        connection: "EmailBackend" = None
        if DEBUG:
            connection = mail.get_connection(
                backend="django.core.mail.backends.console.EmailBackend"
            )
        else:
            host: str = (
                Settings.objects.only("value").get(name="feedback_mailing_host").value
            )
            port: str = (
                Settings.objects.only("value").get(name="feedback_mailing_port").value
            )
            username: str = (
                Settings.objects.only("value").get(name="feedback_mailing_login").value
            )
            password: str = (
                Settings.objects.only("value")
                .get(name="feedback_mailing_password")
                .value
            )
            tls_str: str = (
                Settings.objects.only("value")
                .get(name="feedback_mailing_tls_usage")
                .value
            )
            tls: bool = True if tls_str.lower() == "y" else False
            ssl_str: str = (
                Settings.objects.only("value")
                .get(name="feedback_mailing_ssl_usage")
                .value
            )
            ssl: bool = True if ssl_str.lower() == "y" else False
            from django.core.mail.backends.smtp import EmailBackend

            connection = EmailBackend(
                host=host,
                port=port,
                username=username,
                password=password,
                use_tls=tls,
                use_ssl=ssl,
                timeout=10,
                fail_silently=False,
            )
        reciever: str = (
            Settings.objects.only("value").get(name="feedback_mailing_email").value
        )
        body: str = "{name}\n{site}\n{msg}".format(
            name=self.cleaned_data["name"],
            site=self.cleaned_data["site"],
            msg=self.cleaned_data["message"],
        )
        connection.open()
        mail.EmailMessage(
            subject="Feedback form message",
            from_email=self.cleaned_data["email"],
            to=[reciever],
            body=body,
            connection=connection,
        ).send(fail_silently=False)
        connection.close()
