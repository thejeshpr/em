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



from .models import (
    Category,    
    Transaction
    )

from .forms import CategoryForm, TransactionForm


class Home(generic.ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'em/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['additional_info'] = helper.get_home_page_data()
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryCreateView(edit.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'em/category-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['page'] = 'car-add'
        # context['title'] = 'Add new car'
        # context['heading'] = 'Add new car'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryUpdateView(edit.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'em/category-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
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
    template_name = 'em/category-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = kwargs.get('object')
        context['ttl_amt'] = obj.transactions.all().aggregate(ttl_amt=Sum('amount')).get('ttl_amt')
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = 'em/category-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        spending = list()

        for category in Category.objects.all():
            overall_amt = Transaction.objects\
                        .aggregate(amount=Sum('amount')).get('amount')
            amount = Transaction.objects\
                        .filter(category=category)\
                        .aggregate(amount=Sum('amount')).get('amount')

            if amount:            
                spending.append({
                        'category': category,
                        'total_amt': amount,
                        'overall_amt': overall_amt,
                        'percentage_share': int((amount / overall_amt) * 100)                        
                    })

        context['categories'] = spending        
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionCreateView(edit.CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'em/transaction-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['page'] = 'car-add'
        # context['title'] = 'Add new car'
        # context['heading'] = 'Add new car'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionUpdateView(edit.UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'em/transaction-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['page'] = 'car-add'
        # context['title'] = 'Add new car'
        # context['heading'] = 'Add new car'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionDeleteView(edit.DeleteView):
    model = Transaction    
    template_name = 'em/delete-confirm.html'
    success_url = reverse_lazy('em:home')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TrasactionDetailView(generic.DetailView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'em/transaction_details.html'


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

    context = TransactionHelper.get_spending(**payload)
    return render(request, 'em/dashboard.html', context=context)

        


class TransactionHelper(object):
    date_fmt = "%Y-%m-%d"

    @staticmethod
    def get_range(days):
        tdy_dt, ystr_dt = date.today(), date.today() - timedelta(days=days)    

        return [
            ystr_dt.strftime(TransactionHelper.date_fmt),
            tdy_dt.strftime(TransactionHelper.date_fmt)
        ]        

    @staticmethod
    def get_daily_spending():
        today_dt = date.today()        
        labels = []
        data = []
        for i in range(1, 7, 1):
            dt = today_dt - relativedelta.relativedelta(days=i)
            labels.append(dt.strftime('%d-%m-%Y'))
            data.append(Transaction.objects.filter(date=dt).aggregate(expense=Sum('amount')).get('expense') or 0)
            # day_dat[dt.strftime('%d-%m-%Y')] = Transaction.objects.filter(date=dt).aggregate(expense=Sum('amount')).get('expense') or 0
        # print(day_dat)
        # print(len(data))
        return labels, data

    @staticmethod
    def get_spending(**kwargs):
        context = {}
        spending = list()
        filters = dict(tran_type='EX')

        ref_dt = datetime.strptime(kwargs.get('ref_dt'), TransactionHelper.date_fmt) if kwargs.get('ref_dt') else date.today()

        if kwargs.get('last_n_days'):            
            filters.update(date__range = TransactionHelper.get_range(int(kwargs.get('last_n_days'))))
            context['selected_range'] = f"Last {kwargs.get('last_n_days')} days"            

        elif kwargs.get('from_dt') and kwargs.get('to_dt'):
            from_dt, to_dt = (
                datetime.strptime(kwargs.get('from_dt'), TransactionHelper.date_fmt),
                datetime.strptime(kwargs.get('to_dt'), TransactionHelper.date_fmt)
            )
            filters.update(date__range = [from_dt, to_dt])
            context['selected_range'] = f"{kwargs.get('from_dt')} - {kwargs.get('to_dt')}"

        elif kwargs.get('ref_dt'):            
            filters.update(date=ref_dt)
            context['selected_range'] = kwargs.get('ref_dt')                 

        else:
            filters.update(date=date.today())
            context['selected_range'] = "Today"

        context['transactions'] = Transaction.objects.filter(**filters).order_by('-date', '-pk')
        context['delta'] = kwargs.get("delta")
        context['ref_dt'] = datetime.strftime(ref_dt, TransactionHelper.date_fmt)
        context['prev'] = ref_dt - relativedelta.relativedelta(days=1)
        context['next'] = ref_dt + relativedelta.relativedelta(days=1)

        overall_expns = Transaction.objects.filter(**filters)\
                            .aggregate(expense=Sum('amount'))\
                            .get('expense')        

        for category in Category.objects.all():
            amount = Transaction.objects\
                        .filter(category=category, **filters)\
                        .aggregate(amount=Sum('amount')).get('amount')

            if amount:            
                spending.append({
                        'category': category,
                        'total_amt': amount,
                        'percentage': int((amount / overall_expns) * 100)                        
                    })
        
        context['spendings'] = spending
        context['total_expense'] = overall_expns
        
        context["label"], context["data"] = TransactionHelper.get_daily_spending()
        return context

        
