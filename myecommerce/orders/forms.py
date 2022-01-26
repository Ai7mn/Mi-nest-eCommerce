from django import forms
from django.forms import ModelForm
from .models import Payment



class UploadPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_slip']