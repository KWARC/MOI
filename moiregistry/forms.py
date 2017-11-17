from django import forms
from .models import ObjectRegistration


class ObjectRequestForm(forms.ModelForm):
    class Meta:
        model = ObjectRegistration
        fields = ('type', 'note', 'keywords', 'modref',)