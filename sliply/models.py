from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse

PAYMENT_TYPES = (
    (0, 'Cash'),
    (1, 'Card'),
    (2, 'Other'),
)

class Slip(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    scanfile = models.FileField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    raw_text = models.TextField(null=True, blank=True)
    seller_name = models.CharField(max_length=255, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    payment_type = models.SmallIntegerField(choices=PAYMENT_TYPES, null=True)
    # address = models.ForeignKey('Address', null=True, blank=True)
    # group = models.ManyToManyField('Group', blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('slip_details', kwargs = {'pk': self.pk})


class Item(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    slip = models.ForeignKey(Slip)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    raw_text = models.TextField(null=True, blank=True)
    item_name = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # category

    def __str__(self):
        return self.item_name