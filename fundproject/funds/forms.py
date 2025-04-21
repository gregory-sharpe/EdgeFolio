# funds/forms.py

from django import forms
from .models import Fund


class FundUploadForm(forms.Form):

    """
    Simple form with one FileField to upload a CSV of Funds.
    Expected CSV columns: name, strategy, aum, inception_date (YYYY-MM-DD)
    """
    # TODO Upload size should be set as an environment variable
    MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB

    REQUIRED_HEADERS = {"name", "strategy", "aum", "inception_date"}

    file = forms.FileField(
        label="Select CSV file",
        help_text="Upload a CSV matching the sample_fund_data structure.",
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )

    def clean_file(self):
        # TODO make it so the csv file is positionally invariant if there is a header.
        # TODO run a test on the first and last row and fail if it doesnt work.
        # TODO User friendly error template but dont fully implement.
        # TODO add a test forms file.
        # TODO if a unique value is used, on the upload form let the user know.
        # TODO potentially add a upload report with details on failures, defaults etc
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.lower().endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed.")
        if uploaded_file.size > self.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("File should be no larger than 2MB.")
        return uploaded_file


class FundForm(forms.ModelForm):
    """
    Form for creating/editing individual Fund records.
    """
    class Meta:
        model = Fund
        fields = ['name', 'strategy', 'aum', 'inception_date']
        widgets = {
            'inception_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }
        help_texts = {
            'name':     "Name of the fund (unique).",
            'strategy': "Select one of the predefined strategies.",
            'aum':      "Assets Under Management in USD (positive, up to 2 decimals).",
            'inception_date': "Date the fund was launched. Defaults to today if left blank.",
        }
