from django import forms

from .models import Rate

class RateForm(forms.ModelForm):

    class Meta:
        model = Rate
        # возможно добавить "lot"
        fields = ('sum_rate',)