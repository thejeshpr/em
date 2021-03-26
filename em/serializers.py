from rest_framework import serializers

from .models import Category, Transaction

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'icon']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'category', 'date', 'desc']