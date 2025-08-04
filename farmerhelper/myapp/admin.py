from django.contrib import admin
from .models import Crop,Expense,Harvest

admin.site.register(Crop)
admin.site.register(Expense)
admin.site.register(Harvest)
# Register your models here.
