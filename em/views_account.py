# import datetime
from datetime import date, timedelta, datetime


from django.db.models import Sum, Count
# from dateutil.relativedelta import relativedelta
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import edit
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from dateutil import relativedelta


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch, mm, pica, toLength


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg, Count, Min, Sum

from .models import Account, Transaction, Category

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
        context["statements"] = AccountHelper.get_act_statments(context["account"].name)
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

@login_required(login_url='/login/')
def file_download(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    # buffer.seek(0)

    can = canvas.Canvas(buffer, pagesize=letter)
    can.setLineWidth(.3)
    can.setFont('Helvetica', 12)
    # can.drawString(30,750,'OFFICIAL COMMUNIQUE')
    # can.drawString(30,735,'OF ACME INDUSTRIES')
    # can.drawString(500,750,"12/12/2010")
    # can.line(480,747,580,747)
    # can.drawString(275,725,'AMOUNT OWED:')
    # can.drawString(500,725,"$1,000.00")
    # can.line(378,723,580,723)
    # can.drawString(30,703,'RECEIVED BY:')
    # can.line(120,700,580,700)
    # can.drawString(120,703,"JOHN DOE")
    # https://code-maven.com/creating-pdf-files-using-python

    can.drawString(3.8 * inch, 725,'Transactions')
    can.line(30,715,580,715)

    for i in range(10):
        can.drawString(cm, 695 - i * 12, f'{i}: Transactions')

    can.save()

    buffer.seek(0)


    return FileResponse(buffer, as_attachment=True, filename='form.pdf')


@login_required(login_url='/login/')
def json_download(request, entity):
    valid_entities = {
            'transaction': Transaction,
            'category': Category,
            'account': Account
        }
    if entity in valid_entities.keys():
        objects = valid_entities[entity].objects.all().order_by('-pk')
        objects = serializers.serialize('json', objects)        
        return HttpResponse(objects, content_type="text/json")
    else:
        return HttpResponseBadRequest()
