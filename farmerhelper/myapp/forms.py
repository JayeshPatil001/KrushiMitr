from django import forms
from .models import Crop, Harvest, Expense


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'variety', 'season']

class HarvestForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = ['crop', 'date_of_harvest', 'buyer', 'rate_per_unit', 'quantity']
        widgets = {
            'date_of_harvest': forms.DateInput(attrs={'type': 'date'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['crop', 'reason', 'amount', 'date']
        widgets = {
        'date': forms.DateInput(attrs={'type': 'date'}),
}

