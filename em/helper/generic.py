from datetime import date, timedelta, datetime

from dateutil import relativedelta

from . import (
    AccountHelper,
    BudgetHelper,
    CategoryHelper,
    TransactionHelper
)


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
        
        if kwargs.get('ref_dt'):
            ref_dt = datetime.strptime(kwargs.get('ref_dt'), Helper.date_fmt)
        else:
            ref_dt = date.today()


        filters, context['selected_range'] = Helper.get_filters(**kwargs)
        context['ref_dt'] = datetime.strftime(ref_dt, Helper.date_fmt)
        context['prev'] = ref_dt - relativedelta.relativedelta(days=1)
        context['next'] = ref_dt + relativedelta.relativedelta(days=1)
        
        context['budget'] = BudgetHelper.get_current_month_budget()
        context['current_month_expense'] = TransactionHelper.get_current_month_expense()

        if context['budget'] and context['current_month_expense']:
            context['budget_difference'] = context['budget'] - context['current_month_expense']
        else:
            context['budget_difference'] = 0

        context['transactions'] = TransactionHelper.get_transactions(**filters)
        context['total_expense'] = TransactionHelper.get_expenses(**filters)        
        context['spendings'], context['cat_values'], context['cat_labels'] = CategoryHelper.get_categories_expense(**filters)                     
        context["tran_labels"], context["tran_values"] = TransactionHelper.get_spendings_of(7)
        context["account_spendings"], context["account_labels"], context["account_values"] = AccountHelper.get_spendings(**filters)
        return context

    @staticmethod
    def get_filters(**kwargs):
        filters = dict()
        filter_text: str = ""
        ref_dt = datetime.strptime(kwargs.get('ref_dt'), Helper.date_fmt) if kwargs.get('ref_dt') else date.today()
        
        if kwargs.get('last_n_days'):            
            filters.update(date__range = Helper.get_range(int(kwargs.get('last_n_days'))))            
            filter_text = f"Last {kwargs.get('last_n_days')} days"

        elif kwargs.get('from_dt') and kwargs.get('from_dt'):
            from_dt, to_dt = (
                datetime.strptime(kwargs.get('from_dt'), Helper.date_fmt),
                datetime.strptime(kwargs.get('to_dt'), Helper.date_fmt)
            )
            filters.update(date__range = [from_dt, to_dt])            
            filter_text = f"{kwargs.get('from_dt')} - {kwargs.get('to_dt')}"

        elif kwargs.get('ref_dt'):            
            filters.update(date=ref_dt)
            filter_text = kwargs.get('ref_dt')                 

        else:
            filters.update(date=date.today())
            filter_text = "Today"

        return filters, filter_text
