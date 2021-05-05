from datetime import date, datetime

from dateutil import relativedelta
from django.db.models import Sum, Count

from em.models import Budget


class BudgetHelper(object):
    date_fmt = "%m-%Y"

    @staticmethod
    def get_current_month_budget():
        return Budget.objects.filter(
                date__month=date.today().month,
                date__year=date.today().year
            ).aggregate(budget=Sum('amount')).get('budget') or 0

    @staticmethod
    def get_budget_list_view(ref_month):
        context = dict()
        dt = datetime.strptime(ref_month, BudgetHelper.date_fmt) if ref_month else date.today()
        context['total_budget'] = Budget.objects.filter(
                                        date__month=dt.month,
                                        date__year=dt.year
                                    )\
                                    .aggregate(budget=Sum('amount'))\
                                        .get('budget') or 0
        context['prev_month'] = dt - relativedelta.relativedelta(months=1)
        context['next_month'] = dt + relativedelta.relativedelta(months=1)
        context['cur_month'] = dt
        return context