from django import forms

class Extendeduserform(forms.Form):
    file = forms.FileField()
    phone = forms.CharField(label='Phoneno', max_length=100)
    adress = forms.CharField(label='Adress', max_length=100)