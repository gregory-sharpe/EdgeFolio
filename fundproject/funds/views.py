from django.shortcuts import render, redirect
from .forms import FundUploadForm  # , FundForm
from .models import Fund
# from .forms import FundCSVUploadForm
from django.db.models import Sum
import csv
import io
from django.core.exceptions import ValidationError


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

# reliant on columns being exact

# Views probably shouldn't be this bloated


def upload_funds(request):
    form = FundUploadForm()

    if request.method == 'POST':
        form = FundUploadForm(request.POST, request.FILES)
        print("checking for valid form")
        if form.is_valid():
            # You can add logic to handle the file after it is validated and saved
            # For now, we just print the cleaned data

            uploaded_file = form.cleaned_data['file']
            decoded_file = uploaded_file.read().decode(
                'utf-8-sig')  # -sig ignores Byte Order Mark (BOM)
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            # 2 Options:
            # Bulk upload - no validation. no partial completion
            # Validate each seperately
            validated_funds = []
            invalid_funds = []
            for row in reader:
                print("showing row")
                print(row)
                fund = Fund(
                    name=row.get('Name'),
                    strategy=row.get('Strategy'),
                    aum=row.get('AUM (USD)'),
                    inception_date=row.get('Inception Date')
                )
                try:
                    fund.full_clean()
                    fund.save()
                    validated_funds.append(fund)
                except ValidationError as e:
                    invalid_funds.append((fund, e.message_dict))
                    print(f"{e}: at {fund}")
                # fund_objects.append(fund)
            # Fund.objects.bulk_create(validated_funds)
            print(f"Number of errors: {len(invalid_funds)}")
            return render(request, 'funds/error_report.html',  # include a report page for the upload
                          {
                              'file_name': uploaded_file.name,
                              'invalid_funds_E': invalid_funds,
                              # all types of errors that appeard


                          })

    return render(request, 'funds/upload_funds.html', {'form': form})
