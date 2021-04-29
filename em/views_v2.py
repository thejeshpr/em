

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator


@login_required(login_url='/login/')
def dashboard(request):    
    payload = dict(
        last_n_days=request.GET.get('last_n_days'),
        ref_dt=request.GET.get('ref_dt'),
        delta=int(request.GET.get('delta', 0)),
        from_dt=request.GET.get('fromDate'),
        to_dt=request.GET.get('toDate'),
    )
    
    context = Helper.get_data(**payload)    
    return render(request, 'em/dashboard.html', context=context)
