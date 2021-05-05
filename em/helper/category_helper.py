from datetime import date, timedelta, datetime

from django.db.models import Sum

from em.models import Category, Transaction

class CategoryHelper(object):
    date_fmt = "%Y-%m-%d"
    @staticmethod
    def get_categories_expense(**filters):
        filters["tran_type"] = "EX"
        spendings = Transaction.objects.values('category__name', 'category').filter(**filters).annotate(spendings=Sum('amount'))
        labels, values = CategoryHelper.get_graph_data(spendings)
        return spendings, labels, values

    @staticmethod
    def get_graph_data(spendings):
        labels, values = list(), list()

        if spendings:        
            for entry in spendings:
                labels.append(entry.get('spendings'))
                values.append(entry.get('category__name'))

        return labels, values

    
    @staticmethod
    def get_transactions(context, **kwargs):
        category = context['category']
        ref_dt = kwargs.get("ref_dt")        
        
        if ref_dt:
            ref_dt = datetime.strptime(ref_dt, CategoryHelper.date_fmt)
            context['transactions'] = category.transactions.filter(date=ref_dt)
            context['ttl_amt'] = category.transactions.filter(date=ref_dt).aggregate(ttl_amt=Sum('amount')).get('ttl_amt')            
        else:
            context['transactions'] = category.transactions.all()
            context['ttl_amt'] = category.transactions.all().aggregate(ttl_amt=Sum('amount')).get('ttl_amt')
        return context


        