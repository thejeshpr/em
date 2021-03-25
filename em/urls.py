from django.urls import path

from . import views
from . import views_keystore

app_name = 'em'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('category', views.CategoryListView.as_view(), name='category-list'),
    path('category/add', views.CategoryCreateView.as_view(), name='category-add'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category-update'),    
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('transaction/add', views.TransactionCreateView.as_view(), name='transaction-add'),
    path('transaction/<int:pk>', views.TrasactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update', views.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete', views.TransactionDeleteView.as_view(), name='transaction-delete'),

    path('key-store', views_keystore.KSListView.as_view(), name='keystore-list'),
    path('key-store/add', views_keystore.KSCreateView.as_view(), name='keystore-add'),
    path('key-store/<int:pk>', views_keystore.KSDetailView.as_view(), name='keystore-detail'),
    path('key-store/<int:pk>/update', views_keystore.KSUpdateView.as_view(), name='keystore-update'),
    path('key-store/<int:pk>/delete', views_keystore.KSDeleteView.as_view(), name='keystore-delete'),
        
]