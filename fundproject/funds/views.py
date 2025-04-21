from django.shortcuts import render, redirect
# from .forms import FundUploadForm, FundForm
from .models import Fund
# from .forms import FundCSVUploadForm
from django.db.models import Sum
import csv


def fund_list(request):
    strategy_filter = request.GET.get('strategy', None)
    if strategy_filter:
        funds = Fund.objects.filter(strategy=strategy_filter)
    else:
        funds = Fund.objects.all()

    total_funds = funds.count()
    total_aum = funds.aggregate(Sum('aum'))['aum__sum'] or 0

    strategies = Fund.objects.values_list('strategy', flat=True).distinct()

    context = {
        'funds': funds,
        'total_funds': total_funds,
        'total_aum': total_aum,
        'strategies': strategies,
    }
    return render(request, 'funds/fund_list.html', context)


def upload_funds(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(data)

        for row in reader:
            Fund.objects.create(
                name=row['name'],
                strategy=row['strategy'],
                aum=float(row['aum']),
                inception_date=row['inception_date'],
            )
        # Redirect back to the fund list after upload.
        return redirect('fund_list')

    return render(request, 'funds/upload_funds.html')
