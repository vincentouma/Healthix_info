from django import forms
from .models import Payment,Hospitals


class PaymentForm(forms.ModelForm):
    class Meta:
        model  = Payment
        fields = ['name','account','phone_Number','amount']

class HospitalsForm(forms.ModelForm):
    class Meta:
        model  = Hospitals
        fields = ['reference_no',]