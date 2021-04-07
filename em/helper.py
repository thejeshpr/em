from datetime import date, timedelta, datetime
from dateutil import relativedelta

from .models import Transaction


class TransactionHelper(object):
    
    @staticmethod
    def get_transactions(**kwargs):
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
        return context

        
