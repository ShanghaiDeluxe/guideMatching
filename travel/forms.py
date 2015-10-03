from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search for tour spot', widget=forms.TextInput(attrs={'size': 32}))
