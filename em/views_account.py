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

from .helper import AccountHelper


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = list()
        for act in context.get('accounts'):
            spendings = Transaction.objects.filter(account=act)\
                            .aggregate(spendings=Sum('amount'))\
                                .get('spendings')        
            data.append({
                "account": act,
                "spendings": spendings
            })
        context['data'] = data
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AccountDetailView(generic.DetailView):
    model = Account    
    context_object_name = 'account'
    template_name = 'em/account/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return AccountHelper.get_account_details(            
            context=context,
            ref_month=self.request.GET.get('ref_month'),
            from_dt=self.request.GET.get('fromDate'),
            to_dt=self.request.GET.get('toDate')
        )
        

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AccountUpdateView(edit.UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'em/account/edit.html'    


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


