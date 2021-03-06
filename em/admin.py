# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Account,
    Budget,
    Category,
    Transaction,
    KeyStore    
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


@admin.register(KeyStore)
class KeyStoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')
    search_fields = ('key',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'typ')
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