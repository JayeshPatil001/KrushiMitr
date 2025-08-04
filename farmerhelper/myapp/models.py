from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from .validator import validate_only_letters


class Crop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100,validators=[validate_only_letters])
    variety = models.CharField(max_length=100, blank=True, null=True,validators=[validate_only_letters])
    season = models.CharField(max_length=50, blank=True, null=True,validators=[validate_only_letters])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_expense(self):
        return self.expenses.aggregate(total=Sum('amount'))['total'] or 0

    def total_sale(self):
        return self.harvests.aggregate(total=Sum('total_amount'))['total'] or 0

    def profit(self):
        return self.total_sale() - self.total_expense()


class Harvest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    crop = models.ForeignKey(Crop, related_name='harvests', on_delete=models.CASCADE)
    date_of_harvest = models.DateField()
    buyer = models.CharField(max_length=100,validators=[validate_only_letters])
    rate_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.rate_per_unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.crop.name} sold to {self.buyer} on {self.date_of_harvest}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    crop = models.ForeignKey(Crop, related_name='expenses', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255,validators=[validate_only_letters])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.reason} - ₹{self.amount} on {self.date}"

