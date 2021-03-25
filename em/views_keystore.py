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

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg, Count, Min, Sum

from .models import (KeyStore)

from .forms import KeyStoreForm


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class KSCreateView(edit.CreateView):
    model = KeyStore
    form_class = KeyStoreForm
    template_name = 'em/key-store_create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class KSDetailView(generic.DetailView):
    model = KeyStore    
    context_object_name = 'keystore'
    template_name = 'em/key-store_details.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class KSUpdateView(edit.UpdateView):
    model = KeyStore
    form_class = KeyStoreForm
    template_name = 'em/key-store_create.html'    


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class KSDeleteView(edit.DeleteView):
    model = KeyStore    
    template_name = 'em/delete-confirm.html'
    success_url = reverse_lazy('em:keystore-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class KSListView(generic.ListView):
    model = KeyStore    
    template_name = "em/key-store_list.html"
    context_object_name = "keystores"


