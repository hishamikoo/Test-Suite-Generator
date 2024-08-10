from django import forms
from .models import Suite, Task # Note the relative import . you can also use .. to go 2 up


class SuiteForm(forms.ModelForm):
    language = forms.ChoiceField(choices=Task.LANGUAGE_CHOICES)
    number = forms.IntegerField(min_value=1)
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Create a password (optional)'}))

    class Meta:
        model = Suite
        fields = ["language", "number", "password"]


class ProtectedSuiteForm(forms.ModelForm):
    password = forms.CharField(required=True,widget=forms.PasswordInput())
    class Meta:
        model = Suite
        fields = ["password"]
