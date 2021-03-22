from django import forms
from .models import Pilot

class PilotForm(forms.ModelForm):
    class Meta:
        model = Pilot
        fields = '__all__'