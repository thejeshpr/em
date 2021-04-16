from datetime import date, datetime
from typing import Any, Dict

from dateutil import relativedelta
from django.db.models import Sum, Count

from em.models import Account, Transaction


class AccountHelper(object):
    date_fmt = '%m-%Y'
    day_fmt = '%Y-%m-%d'

    @staticmethod
    def get_spendings(overall_expns, **filters):                
        spendings = list()
        account_labels = list()
        account_values = list()

        if overall_expns:
            for account in Account.objects.all():
                amount = Transaction.objects\
                            .filter(account=account, **filters)\
                            .aggregate(amount=Sum('amount')).get('amount')

                if amount:
                    spendings.append({
                        'account': account,
                        'spendings': amount,
                        'percentage': int((amount / overall_expns) * 100)
                    })
                    account_labels.append(account.name)
                    account_values.append(amount)
        return spendings, account_labels, account_values

    @staticmethod
    def get_account_details(context: Dict[Any, Any], **kwargs):        
        ref_month = kwargs.get('ref_month')
        account: Account = context.get('account')
        # today = date.today()
        # print(today.day, account.statement_date, today.day > account.statement_date)

        filters = dict()
        dt = datetime.strptime(ref_month, AccountHelper.date_fmt) if ref_month else date.today()

        if kwargs.get('from_dt') and kwargs.get('to_dt'):
            from_dt, to_dt = (
                datetime.strptime(kwargs.get('from_dt'), AccountHelper.day_fmt),
                datetime.strptime(kwargs.get('to_dt'), AccountHelper.day_fmt)
            )
            filters.update(date__range = [from_dt, to_dt])
            context['selected_range'] = f"{kwargs.get('from_dt')} - {kwargs.get('to_dt')}"

        else:            
            context['selected_range'] = datetime.strftime(dt, '%m-%Y')

            filters = dict(
                date__month=dt.month,
                date__year=dt.year
            )

        context['prev_month'] = dt - relativedelta.relativedelta(months=1)
        context['next_month'] = dt + relativedelta.relativedelta(months=1)
        context['cur_month'] = dt
        context['spendings'] = Transaction.objects\
                                .filter(account=account, **filters)\
                                    .aggregate(spendings=Sum('amount'))\
                                        .get('spendings')   
        context['transactions'] = Transaction.objects.filter(account=account, **filters).order_by("-date")
        return context        

