from calendar import monthrange
from datetime import date, timedelta, datetime

from dateutil import relativedelta

from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import edit
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg, Count, Min, Sum

from .models import Transaction, Budget
from .forms import BudgetForm
from .helper import BudgetHelper


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BudgetCreateView(edit.CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'em/budget/create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BudgetDetailView(generic.DetailView):
    model = Budget
    context_object_name = 'budget'
    template_name = 'em/budget/details.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BudgetUpdateView(edit.UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'em/budget/update.html'    


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BudgetDeleteView(edit.DeleteView):
    model = Budget    
    template_name = 'em/delete-confirm.html'
    success_url = "/"


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BudgetListView(generic.ListView):
    model = Budget
    context_object_name = "budgets"
    template_name = 'em/budget/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ref_month = self.request.GET.get("ref_month")
        data = BudgetHelper.get_budget_list_view(ref_month)        
        return {**context, **data}

    def get_queryset(self, **kwargs):
        date_fmt = "%m-%Y"
        ref_month = self.request.GET.get("ref_month")
        dt = datetime.strptime(ref_month, date_fmt) if ref_month else date.today()
        return Budget.objects.filter(date__month=dt.month, date__year=dt.year)
