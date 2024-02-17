from django import forms
class Resume(forms.Form):
    file=forms.FileField()