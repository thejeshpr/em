from django.urls import path

from . import views
from . import views_transaction
from . import views_account
from . import views_budget


app_name = 'em'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('category', views.CategoryListView.as_view(), name='category-list'),
    path('category/add', views.CategoryCreateView.as_view(), name='category-add'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category-update'),    
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('transaction/add', views.TransactionCreateView.as_view(), name='transaction-add'),
    path('transaction/summary', views_transaction.transactions_day_view, name='transaction-summary'),
    path('transaction/summary-month', views_transaction.transactions_month_view, name='transaction-summary-month'),
    path('transaction/<int:pk>', views.TrasactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update', views.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete', views.TransactionDeleteView.as_view(), name='transaction-delete'),

    path('account', views_account.AccountListView.as_view(), name='account-list'),
    path('account/add', views_account.AccountCreateView.as_view(), name='account-add'),
    path('account/<int:pk>', views_account.AccountDetailView.as_view(), name='account-detail'),
    path('account/<int:pk>/update', views_account.AccountUpdateView.as_view(), name='account-update'),        

    path('budget', views_budget.BudgetListView.as_view(), name='budget-list'),
    path('budget/add', views_budget.BudgetCreateView.as_view(), name='budget-add'),
    path('budget/<int:pk>', views_budget.BudgetDetailView.as_view(), name='budget-detail'),
    path('budget/<int:pk>/update', views_budget.BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/<int:pk>/delete', views_budget.BudgetDeleteView.as_view(), name='budget-delete'),


    path('test', views.test, name='test'),
    path('test-download', views_account.file_download, name="test-download"),
    path('json/<str:entity>', views_account.json_download, name="json-download"),
            
    path('chart/transactions', views.ChartTransaction.as_view(), name='chart-transactions'),
]