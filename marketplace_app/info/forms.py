from django import forms

from info.models import SEOItem
from info.utils import get_urls


def get_choices():
    return [(item, item) for item in get_urls()]


class SEOItemForm(forms.ModelForm):
    """Форма редактирования модели SEO
    """

    def __init__(self, *args, **kwargs):
        super(SEOItemForm, self).__init__(*args, **kwargs)
        self.fields["path_name"].widget = forms.Select(choices=get_choices())

    class Meta:
        model = SEOItem
        fields = "__all__"