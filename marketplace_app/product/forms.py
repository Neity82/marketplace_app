from django import forms
from import_export.forms import ImportForm

from product.models import ProductReview
from shop.models import Shop


class ProductReviewForm(forms.ModelForm):
    """Форма для создания нового отзыва."""

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "name": "text",
                "id": "text",
                "placeholder": "Review",
            }),
    )

    class Meta:
        model = ProductReview
        fields = "__all__"


class CustomImportForm(ImportForm):
    """
    Форма для выбора магазина при импорте
    на панели администратора
    """
    shop = forms.ModelChoiceField(
        queryset=Shop.objects.all(),
        required=False)


