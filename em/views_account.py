# import datetime
from datetime import date, timedelta, datetime


from django.db.models import Sum, Count
# from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import edit
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from dateutil import relativedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg, Count, Min, Sum

from .models import Account, Transaction

from .forms import AccountForm


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AccountCreateView(edit.CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'em/account/create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AccountListView(generic.ListView):
    model = Account
    context_object_name = "accounts"
    template_name = 'em/account/list.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AccountDetailView(generic.DetailView):
    model = Account    
    context_object_name = 'account'
    template_name = 'em/account/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        act = context.get('account')
        
        ref_month = self.request.GET.get('ref_month')
        
        dt_fmt = '%m-%Y'
        dt = datetime.strptime(ref_month, dt_fmt) if ref_month else date.today()
        
        filters = dict(
            date__month=dt.month,
            date__year=dt.year
        )
        context['prev_month'] = dt - relativedelta.relativedelta(months=1)
        context['next_month'] = dt + relativedelta.relativedelta(months=1)
        context['cur_month'] = dt
        context['spendings'] = Transaction.objects\
                                .filter(account=act, **filters)\
                                    .aggregate(spendings=Sum('amount'))\
                                        .get('spendings')        
        return context


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class KSUpdateView(edit.UpdateView):
#     model = KeyStore
#     form_class = KeyStoreForm
#     template_name = 'em/key-store_create.html'    


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class KSDeleteView(edit.DeleteView):
#     model = KeyStore    
#     template_name = 'em/delete-confirm.html'
#     success_url = reverse_lazy('em:keystore-list')


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class KSListView(generic.ListView):
#     model = KeyStore    
#     template_name = "em/key-store_list.html"
#     context_object_name = "keystores"


