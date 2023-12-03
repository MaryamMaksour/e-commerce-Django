from django import forms
from django_countries.fields import CountryField


CITY = (
    ('Sc', 'Select city'),
    ('Ha', 'Hama'),
    ('Dm', 'Damascus'),
    ('Al', 'Aleppo' ),
    ('Hm', 'Homs'), 
    ('Lt', 'Latakia'),
    ('Tr', 'Tartus' ),
    ('Dr', 'Daraa'),
    ('Su', 'Al-Suwayda'),
    ('Hs', 'Al-Hasakah'),
    ('Qm', 'Al-Qamishli'),
    ('Rq', 'Al-Raqqah'),
    ('Qu', 'Al-Qunaytirah'),
    ('Dz', 'Dayr al-Zawr'),
    ('Id', 'Idlib'),
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_city = forms.ChoiceField(
        required=False,
        choices=CITY)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
   

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


