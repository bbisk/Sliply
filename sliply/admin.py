from django.contrib import admin

# Register your models here.
from .models import Slip, Item

admin.site.register(Slip)
admin.site.register(Item)