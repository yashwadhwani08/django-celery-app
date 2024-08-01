from django import forms

class TextInputForm(forms.Form):
    text_input_1 = forms.CharField(required=False, widget=forms.TextInput(attrs={"size": "40"}))
    text_input_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"size": "40"}))
    text_input_3 = forms.CharField(required=False, widget=forms.TextInput(attrs={"size": "40"}))

