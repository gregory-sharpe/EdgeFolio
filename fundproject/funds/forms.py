# funds/forms.py

from django import forms
from .models import Fund

# TODO make it so the csv file is positionally invariant if there is a header.
# TODO run a test on the first and last row and fail if it doesnt work.
# TODO User friendly error template but dont fully implement.
# TODO add a test forms file.
# TODO if a unique value is used, on the upload form let the user know.
# TODO potentially add a upload report with details on failures, defaults etc


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
        help_text="""Upload a CSV containing four columns:
            Name ,Strategy, AUM, and Inception Date.""",
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )

    def clean_file(self):
        print("Running clean_file")
        uploaded_file = self.cleaned_data['file']
        print(f"File Size: {uploaded_file.size}")
        errors = []
        if not uploaded_file.name.lower().endswith('.csv'):
            # raise forms.ValidationError("Only CSV files are allowed.")
            errors.append("Only CSV files are allowed")
        if uploaded_file.size > self.MAX_UPLOAD_SIZE:
            # raise forms.ValidationError("File should be no larger than 2MB.")
            errors.append("File should be no larger than 2MB.")

        if errors:
            raise forms.ValidationError(errors)
        return uploaded_file
