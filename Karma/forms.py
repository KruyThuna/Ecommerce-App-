from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    payment_proof = forms.ImageField(required=False)  # Add this line
