from django import forms

from product.models import ProductReview


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



