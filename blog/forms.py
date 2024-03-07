from django import forms


class UserInputForm(forms.Form):
    phrase = forms.CharField(label='Enter a phrase', max_length=100)
    export_format = forms.ChoiceField(
        label='Select export format',
        choices=[('csv', 'CSV'), ('xls', 'XLS'), ('json', 'JSON')],
        initial='csv',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
