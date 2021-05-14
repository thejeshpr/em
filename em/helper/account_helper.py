from datetime import date, datetime
from typing import Any, Dict

from dateutil import relativedelta
from django.db.models import Sum, Count

from em.models import Account, Transaction
from .transaction_helper import TransactionHelper


class AccountHelper(object):
    date_fmt = '%m-%Y'
    day_fmt = '%Y-%m-%d'

    @staticmethod
    def get_spendings(**filters):        
        spendings = Transaction.objects.values('account__name', 'account').filter(**filters).annotate(spendings=Sum('amount'))
        labels, values = AccountHelper.get_graph_data(spendings)
        return spendings, labels, values

    @staticmethod
    def get_graph_data(spendings):
        labels, values = list(), list()

        if spendings:        
            for entry in spendings:
                labels.append(entry.get('account__name'))
                values.append(entry.get('spendings'))

        return labels, values


    @staticmethod
    def get_filters(**kwargs):
        filters = dict()    
        # context = dict()
        ref_month = kwargs.get('ref_month')
        dt = datetime.strptime(ref_month, AccountHelper.date_fmt) if ref_month else date.today()

        if kwargs.get('from_dt') and kwargs.get('to_dt'):
            from_dt, to_dt = (
                datetime.strptime(kwargs.get('from_dt'), AccountHelper.day_fmt),
                datetime.strptime(kwargs.get('to_dt'), AccountHelper.day_fmt)
            )
            filters.update(date__range = [from_dt, to_dt])
            selected_range = f"{kwargs.get('from_dt')} - {kwargs.get('to_dt')}"

        else:
            selected_range = datetime.strftime(dt, '%m-%Y')
            filters = dict(
                date__month=dt.month,
                date__year=dt.year
            )

        return filters, selected_range
        
    @staticmethod
    def get_account_details(context: Dict[Any, Any], **kwargs):        
        account: Account = context.get('account')     
        ref_month = kwargs.get('ref_month')
        dt = datetime.strptime(ref_month, AccountHelper.date_fmt) if ref_month else date.today()   
        filters, selected_range = AccountHelper.get_filters(**kwargs)
        context['selected_range'] = selected_range
        context['prev_month'] = dt - relativedelta.relativedelta(months=1)
        context['next_month'] = dt + relativedelta.relativedelta(months=1)
        context['cur_month'] = dt
        context['expenses'] = TransactionHelper.get_expenses(account=account, **filters)
        print(context['expenses'])
        context['transactions'] = TransactionHelper.get_transactions(account=account, **filters)
        return context        

    @staticmethod
    def get_act_statments(account):
        """
        # ?fromDate=2021-03-16&toDate=2021-04-14
        """
        statments = dict()

        if account.act_type == 'credit':
            day = account.statement_date
            for i in range(5):
                ref_dt = date.today() - relativedelta.relativedelta(months=i)
                to_dt = date(ref_dt.year, ref_dt.month, day)
                from_dt = to_dt - relativedelta.relativedelta(months=1)
                from_dt = from_dt + relativedelta.relativedelta(days=1)
                qp = f'?fromDate={from_dt.strftime("%Y-%m-%d")}&toDate={to_dt.strftime("%Y-%m-%d")}'
                statments[f'{from_dt.strftime("%b")}-{to_dt.strftime("%b")}'] = qp

        return statments
