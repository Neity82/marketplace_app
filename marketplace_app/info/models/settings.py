from django.db import models
from django.utils.translation import gettext_lazy as _


class Settings(models.Model):
    name = models.CharField(_("name"), max_length=50)
    value = models.PositiveIntegerField(_("value"), default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = _("settings")
        verbose_name_plural = _("settings")

    def __str__(self):
        return "{name}".format(
            name=self.name
        )
