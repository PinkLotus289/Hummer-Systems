from django import forms

class PhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=20, label="Номер телефона")

class CodeForm(forms.Form):
    phone_number = forms.CharField(widget=forms.HiddenInput())
    code = forms.CharField(max_length=4, label="Код")

class UseInviteForm(forms.Form):
    invite_code = forms.CharField(max_length=6, label="Инвайт-код")
