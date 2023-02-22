from django import forms
class shopregform(forms.Form):
    shop_name = forms.CharField(max_length=30)
    location = forms.CharField(max_length=100)
    idm = forms.IntegerField()
    mail = forms.EmailField()
    ph = forms.IntegerField()
    password = forms.CharField(max_length=20)
    cfmpass= forms.CharField(max_length=20)
class shoplogform(forms.Form):
    shop_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20)

class productform(forms.Form):
    productname=forms.CharField(max_length=30)
    price=forms.IntegerField()
    discription=forms.CharField(max_length=100)
    image=forms.FileField()

class customer_details(forms.Form):
    card_holder_name = forms.CharField(max_length=50)
    card_number = forms.IntegerField
    date = forms.CharField(max_length=50)
    security_code = forms.IntegerField()