from django import forms
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "full_name",
            "email",
            "street_adress",
            "apartment_adress",
            "country",
            "city",
            "zip_code",
        ]
        exclude = ["user"]
