# import datetime
from datetime import date, timedelta, datetime

from dateutil import relativedelta

from django.db.models import Sum, Count
# from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import edit
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg, Count, Min, Sum

from .helper import Helper, CategoryHelper

from pprint import pprint



from .models import (
    Account,
    Budget,
    Category,
    Transaction
)

from .forms import CategoryForm, TransactionForm


class Home(generic.ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'em/index.html'    


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryCreateView(edit.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'em/category/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Create Category"
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryUpdateView(edit.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'em/category/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Update Category"
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryDeleteView(edit.DeleteView):
    model = Category    
    template_name = 'em/delete-confirm.html'
    success_url ="/"


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryDetailView(generic.DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'em/category/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ref_dt = self.request.GET.get('ref_dt')        
        return CategoryHelper.get_transactions(context, ref_dt=ref_dt)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = 'em/category/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['overall_expense'] = Transaction.objects.aggregate(spendings=Sum('amount')).get('spendings')
        return context

    def get_queryset(self, **kwargs):
        fields = [
            'category__name',
            'category',
            'category__icon'            
        ]
        return Transaction.objects.values(*fields).annotate(spendings=Sum('amount')).all()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionCreateView(edit.CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'em/transaction/create.html'    


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionUpdateView(edit.UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'em/transaction/create.html'    


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionDeleteView(edit.DeleteView):
    model = Transaction    
    template_name = 'em/delete-confirm.html'
    success_url = reverse_lazy('em:home')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TrasactionDetailView(generic.DetailView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'em/transaction/details.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionDeleteView(edit.DeleteView):
    model = Transaction    
    template_name = 'em/delete-confirm.html'
    success_url ="/"


@login_required(login_url='/login/')
def dashboard(request):    
    payload = dict(
        last_n_days=request.GET.get('last_n_days'),
        ref_dt=request.GET.get('ref_dt'),
        delta=int(request.GET.get('delta', 0)),
        from_dt=request.GET.get('fromDate'),
        to_dt=request.GET.get('toDate'),
    )
    
    context = Helper.get_data(**payload)
    return render(request, 'em/dashboard.html', context=context)

        

        
@login_required(login_url='/login/')
def test(request):            
    return render(request, 'em/base_test.html')



@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ChartTransaction(generic.ListView):
    model = Transaction
    context_object_name = "tranactions"
    template_name = 'em/chart/chart_transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        res = { entry.get('date').strftime('%d-%b'):entry.get('spendings') for entry in context['tranactions'] }
        labels, data = [], []

        for i in reversed(range(Transaction.objects.count())):
            dt = date.today() - relativedelta.relativedelta(days=i)
            key = dt.strftime('%d-%b')
            labels.append(key)
            data.append(res.get(key, 0))
        context['labels'] = labels
        context['data'] = data

        # from pprint import pprint
        # pprint(context)
        return context

    def get_queryset(self, **kwargs):        
        return Transaction.objects.values('date').annotate(spendings=Sum('amount'))