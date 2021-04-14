from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon = models.CharField(max_length=50, default='las la-question-circle', blank=True, null=True)
    name = models.CharField(max_length=20, unique=True)


    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Category: {self.name}>'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):        
        return reverse('em:home')


class Account(models.Model):
    ACT_TYPE = (
        ('S', 'Savings'),
        ('C', 'Credit')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=200, blank=True, null=True)
    # statement_date = models.IntegerField(help_text="Statement Date", default=1)
    typ = models.CharField(max_length=3, choices=ACT_TYPE)
    

    def __str__(self):
        typ = "SVG" if self.typ == 'S' else "CR"
        return f'{self.name} ({typ})'

    def __repr__(self):
        return f'<Account: {self.name}>'

    def get_absolute_url(self):        
        return reverse('em:account-detail', kwargs=dict(pk=self.pk))


class Transaction(models.Model):
    TRAN_TYPES = (
        ('EX', 'Expense'),
        ('IN', 'Income')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    account = models.ForeignKey('Account', related_name='transactions', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="transactions")
    date = models.DateField(auto_now=False, auto_now_add=False)
    desc = models.TextField(blank=True, null=True)    
    tran_type = models.CharField(max_length=2, choices=TRAN_TYPES, default="EX")
    title = models.CharField(max_length=200,unique_for_date='date')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Transaction: {self.title}>'

    # def save(self, *args, **kwargs):
    #     self.name = self.name.lower()
    #     super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):        
        return reverse('em:home')


class KeyStore(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.key

    def __repr__(self):
        return f'<KeyStore: {self.key}>'

    def get_absolute_url(self):        
        return reverse('em:keystore-list')


