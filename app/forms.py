from django import forms


class HomeForm(forms.Form):
    firstPassage = forms.CharField(widget=forms.Textarea)
    secondPassage = forms.CharField(widget = forms.Textarea)
