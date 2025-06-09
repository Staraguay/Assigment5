from django import forms


class PuzzleForm(forms.Form):
    number = forms.IntegerField(label='Enter a Number', required=True)
    text = forms.CharField(label='Enter a Text Message', max_length=100, required=True)