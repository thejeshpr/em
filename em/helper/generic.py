from datetime import date, timedelta, datetime

from dateutil import relativedelta
from django.db.models import Avg, Count, Min, Sum

from em.models import Account, Category, Transaction, Budget
from . import AccountHelper

class Helper(object):
    date_fmt = "%Y-%m-%d"

    @staticmethod
    def get_range(days):
        tdy_dt, ystr_dt = date.today(), date.today() - timedelta(days=days)    

        return [
            ystr_dt.strftime(Helper.date_fmt),
            tdy_dt.strftime(Helper.date_fmt)
        ]
    
    @staticmethod
    def get_data(**kwargs):
        context = dict()        
        filters = dict(tran_type='EX')

        ref_dt = datetime.strptime(kwargs.get('ref_dt'), Helper.date_fmt) if kwargs.get('ref_dt') else date.today()

        if kwargs.get('last_n_days'):            
            filters.update(date__range = Helper.get_range(int(kwargs.get('last_n_days'))))
            context['selected_range'] = f"Last {kwargs.get('last_n_days')} days"

        elif kwargs.get('from_dt') and kwargs.get('from_dt'):
            from_dt, to_dt = (
                datetime.strptime(kwargs.get('from_dt'), Helper.date_fmt),
                datetime.strptime(kwargs.get('to_dt'), Helper.date_fmt)
            )
            filters.update(date__range = [from_dt, to_dt])
            context['selected_range'] = f"{kwargs.get('from_dt')} - {kwargs.get('to_dt')}"

        elif kwargs.get('ref_dt'):            
            filters.update(date=ref_dt)
            context['selected_range'] = kwargs.get('ref_dt')                 

        else:
            filters.update(date=date.today())
            context['selected_range'] = "Today"

        context['ref_dt'] = datetime.strftime(ref_dt, Helper.date_fmt)
        context['prev'] = ref_dt - relativedelta.relativedelta(days=1)
        context['next'] = ref_dt + relativedelta.relativedelta(days=1)

        # fix it
        context['budget'] = Budget.objects.filter(
                                        date__month=date.today().month,
                                        date__year=date.today().year
                                    ).aggregate(budget=Sum('amount'))\
                                        .get('budget')


        context['current_month_expense'] = Transaction.objects.filter(
                                                date__month=date.today().month,
                                                date__year=date.today().year
                                            ).aggregate(expense=Sum('amount'))\
                                                .get('expense')

        context['budget_difference'] = context['budget'] - context['current_month_expense']


        context['transactions'], context['total_expense'] = TransactionHelper.get_transactions(**filters)        
        # context['spendings'], context['cat_label'], context['cat_data'] = CategoryHelper.get_categories(overall_expns=context["total_expense"], **filters)
        context['spendings'] = CategoryHelper.get_categories(overall_expns=context["total_expense"], **filters)        
        # print(context['spendings'])
        context['cat_data'], context['cat_labels'] = list(), list()
        
        if context['spendings']:
            for entry in context['spendings']:            
                context['cat_data'].append(entry.get('spendings'))
                context['cat_labels'].append(entry.get('category__name'))
        
        context["tran_label"], context["tran_data"] = TransactionHelper.get_spendings_of(7)
        
        context["account_spendings"], context["account_label"], context["account_data"] = AccountHelper.get_spendings(overall_expns=context["total_expense"], **filters)
        return context


class TransactionHelper(object):

    @staticmethod
    def get_transactions(**filters):
        transactions =  Transaction.objects.filter(**filters).order_by("-date", "-pk")        
        overall_expns = Transaction.objects.filter(**filters)\
                            .aggregate(expense=Sum('amount'))\
                            .get('expense') or 0        
        return transactions, overall_expns    

    @staticmethod
    def get_spendings_of(n):        
        labels = []
        data = []
        date_range = [date.today() - relativedelta.relativedelta(days=n), date.today()]
        print(date_range)
        res = Transaction.objects.values('date').filter(date__range=date_range).annotate(spendings=Sum('amount')) #.aggregate(expense=Sum('amount')).get('expense'))
        print(res)
        # print(Transaction.objects.values('category__name').filter(date__range=[ date(2021, 4, 15), date.today() ]).annotate(Sum('amount'))) #.aggregate(expense=Sum('amount')).get('expense'))
        # print(Transaction.objects.values('category__name', 'category').filter(date=date.today()).annotate(spendings=Sum('amount'))) #.aggregate(expense=Sum('amount')).get('expense'))
        data1 = {entry.get('date').strftime('%d-%b'):entry.get('spendings') for entry in res  }
        print(data1)
        for i in reversed(range(n)):
            dt = date.today() - relativedelta.relativedelta(days=i)
            key = dt.strftime('%d-%b')
            labels.append(key)
            data.append(data1.get(key, 0))
            # if dt.strftime('%d-%b') in data1:
            #     data.append(dat)
            # data.append(Transaction.objects.filter(date=dt).aggregate(expense=Sum('amount')).get('expense') or 0)                        
        return labels, data


class CategoryHelper(object):
    @staticmethod
    def get_categories(overall_expns, **filters):
        cat_lables, cat_values, spendings = list(), list(), list()

        if overall_expns:
            return  Transaction.objects.values('category__name', 'category').filter(**filters).annotate(spendings=Sum('amount')) #.aggregate(expense=Sum('amount')).get('expense')                        
            # for category in Category.objects.all():
            #     amount = Transaction.objects\
            #                 .filter(category=category, **filters)\
            #                 .aggregate(amount=Sum('amount')).get('amount')

            #     if amount:            
            #         spendings.append({
            #             'category': category,
            #             'spendings': amount,
            #             'percentage': int((amount / overall_expns) * 100)
            #         })
            #         cat_lables.append(category.name)
            #         cat_values.append(amount)

        # return spendings, cat_lables, cat_values