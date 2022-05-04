from django import forms
from django.db.models.enums import Choices
from .models import PotInt, Energies


class CreateForm(forms.ModelForm):
    class Meta:
        model = PotInt
        fields = ['value','left_bound', 'right_bound']
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class': 'pot-elements'})
        self.fields['left_bound'].widget.attrs.update({'class': 'pot-elements'})
        self.fields['right_bound'].widget.attrs.update({'class': 'pot-elements'})
        

class nForm(forms.Form,):
    def __init__(self, CHOICES = [], *args, **kwargs):
        super(nForm, self).__init__(*args, **kwargs)
        self.fields['n'].choices = CHOICES
    n = forms.ChoiceField(choices= ())