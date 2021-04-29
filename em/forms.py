import datetime

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Budget, Category, Transaction, KeyStore, Account

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
            'account',            
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


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = [
            'name',
            'icon',            
            'typ',
            # 'statement_date',
        ]

    # statement_date = forms.DateField(
    #     # input_formats=['%d/%m/%Y'],
    #     # initial=datetime.date.today
    # )        



class BudgetForm(ModelForm):    
    class Meta:
        model = Budget        
        fields = [
            'title',
            'amount',
            'account',
            'date',
            'category'
        ]
        
    date = forms.DateField(
        # input_formats=['%d/%m/%Y'],
        initial=datetime.date.today
    )
    
