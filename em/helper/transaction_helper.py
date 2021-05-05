from datetime import date, timedelta, datetime

from dateutil import relativedelta
from django.db.models import Sum

from em.models import Transaction


class TransactionHelper(object):

    @staticmethod
    def get_expenses(**filters):
        filters['tran_type'] = 'EX'
        return Transaction.objects.filter(**filters)\
                            .aggregate(expense=Sum('amount'))\
                            .get('expense') or 0

    @staticmethod
    def get_transactions(**filters):
        return Transaction.objects.filter(**filters).order_by("-date", "-pk")        

    @staticmethod
    def get_income(**filters):
        filters['tran_type'] = 'IN'
        return Transaction.objects.filter(**filters).aggregate(income=Sum('amount')).get('income') or 0

    @staticmethod
    def get_spendings_of(n):        
        labels, data, date_range = [], [], [date.today() - relativedelta.relativedelta(days=n), date.today()]
        res = Transaction.objects.values('date').filter(date__range=date_range).annotate(spendings=Sum('amount'))
        res = {entry.get('date').strftime('%d-%b'):entry.get('spendings') for entry in res  }
        
        for i in reversed(range(n)):
            dt = date.today() - relativedelta.relativedelta(days=i)
            key = dt.strftime('%d-%b')
            labels.append(key)
            data.append(res.get(key, 0))

        return labels, data

    @staticmethod
    def get_current_month_expense():
        return Transaction.objects.filter(
                    date__month=date.today().month,
                    date__year=date.today().year
                ).aggregate(expense=Sum('amount')).get('expense') or 0