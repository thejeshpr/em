# import datetime
from datetime import date, timedelta, datetime

from dateutil import relativedelta

from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg, Count, Min, Sum

from .models import Transaction


# class TransactionDayView(generic.ListView):
#     model = Transaction
#     template_name = ''
#     context_object_name = 'transactions'

#     def get_context_data()

@login_required(login_url='/login/')
def transactions_day_view(request):    
    context = dict()
    context['summary'] = Transaction.objects.values('date').annotate(Sum('amount')).order_by('-date')
    context['avg'] = Transaction.objects.aggregate(avg=Avg('amount')).get('avg')
    context['avg'] = int(context['avg']) if context['avg'] else 0
    context['total_amt'] = Transaction.objects.aggregate(amount=Sum('amount')).get('amount')
    return render(request, 'em/transactions/transaction_day-view.html', context=context)


@login_required(login_url='/login/')
def transactions_month_view(request):
    context = dict()    
    dt_fmt = '%m-%Y'

    ref_dt = request.GET.get('ref_dt')
    dt = datetime.strptime(ref_dt, dt_fmt) if ref_dt else date.today()

    filters = dict(
        date__month=dt.month,
        date__year=dt.year
    )
    
    context['prev_month'] = dt - relativedelta.relativedelta(months=1)
    context['next_month'] = dt + relativedelta.relativedelta(months=1)
    context['cur_month'] = dt
    context['summary'] = Transaction.objects.values('date')\
                            .filter(**filters)\
                            .annotate(Sum('amount'))\
                            .order_by('-date')
    context['avg'] = Transaction.objects.filter(**filters).aggregate(avg=Avg('amount')).get('avg')
    context['avg'] = int(context['avg']) if context['avg'] else 0
    context['total_amt'] = Transaction.objects.filter(**filters).aggregate(amount=Sum('amount')).get('amount')
    return render(request, 'em/transactions/transaction_month-view.html', context=context)