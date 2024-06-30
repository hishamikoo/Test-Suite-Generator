from django import forms
from .models import Suite, Task # Note the relative import . you can also use .. to go 2 up


class SuiteForm(forms.ModelForm):
    language = forms.MultipleChoiceField(choices=Task.LANGUAGE_CHOICES)
    number = forms.IntegerField()
    password = forms.CharField(required=False)

    class Meta:
        model = Suite
        fields = ["language", "number", "password"]

class ProtectedSuiteForm(forms.ModelForm):
    password = forms.CharField(required=True)
    class Meta:
        model = Suite
        fields = ["password"]
