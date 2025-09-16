from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(_("Service Title"), max_length=200)
    description = models.TextField(_("Service Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    image = models.ImageField(_("Image"), upload_to='services/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='services', verbose_name=_("Category"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.title