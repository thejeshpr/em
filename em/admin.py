# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Account,
    Budget,
    Category,
    Transaction    
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'title',
        'category',
        'tran_type',
        'date',        
        'created_at',
        'updated_at',
    )
    list_filter = ('category', 'date', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'act_type')
    search_fields = ('name',)


@admin.register(Budget)
class BudgetnAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'title',
        'category',        
        'date',
        'created_at',
        'updated_at',
    )
    list_filter = ('category', 'date', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'