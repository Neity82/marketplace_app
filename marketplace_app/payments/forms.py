from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ["card"]
        widgets = {"card": forms.TextInput(
            attrs={
                "class": "form-input Payment-bill",
                "type": "text",
                "placeholder": "9999 9999",
                "data-mask": "9999 9999",
                "data-validate": "require pay",
            }
        )}

    def clean(self):
        card = self.cleaned_data["card"]
        print(card)
        super().clean()
