import datetime

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import (
    Account,
    Budget,
    Category,
    Transaction    
)

class CategoryForm(ModelForm):    
    class Meta:
        model = Category
        fields = [
            'name',
            'icon'
        ]

    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'em-input'}))
    # icon = forms.CharField(widget=forms.TextInput(attrs={'class': 'em-input'}))


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
    # title = forms.CharField(widget=forms.TextInput(attrs={'class': 'em-input'}))
    desc = forms.CharField(required=False)


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = [
            'name',
            'icon',            
            'act_type',
            'statement_date',
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
    
