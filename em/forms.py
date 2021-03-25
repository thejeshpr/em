import datetime

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Category, Transaction, KeyStore

class CategoryForm(ModelForm):    
    class Meta:
        model = Category
        fields = [
            'name',
            'icon'
        ]        


class TransactionForm(ModelForm):    
    class Meta:
        model = Transaction        
        fields = [
            'title',            
            'amount',
            'date',
            'category',
            'tran_type',
            'desc',
        ]
        
    date = forms.DateField(
        # input_formats=['%d/%m/%Y'],
        initial=datetime.date.today
    )        
    desc = forms.CharField(required=False)

        

class KeyStoreForm(ModelForm):    
    class Meta:
        model = KeyStore
        fields = [
            'key',
            'value'
        ]   