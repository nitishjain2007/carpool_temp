from django import forms

class Extendeduserform(forms.Form):
	image = forms.ImageField(label="Profile Pic")
	phoneno = forms.CharField(label="Phone No", max_length=100)