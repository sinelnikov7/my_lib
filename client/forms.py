from .models import Client
from django.forms import ModelForm, TextInput

class UserForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'sur_name', 'last_name', 'passport_number', 'date', 'email', 'adres']
        widgets = {
            'name': TextInput(attrs={
                'class':'label_style',
                'placeholder':'Имя'
            }),
            'sur_name': TextInput(attrs={
                'class': 'label_style',
                'placeholder': 'Фамилия'
            }),
            'last_name': TextInput(attrs={
                'class': 'label_style',
                'placeholder': 'Отчество'
            }),
            'email': TextInput(attrs={
                'class': 'label_style',
                'placeholder': 'Email',
                'type':'email'
            }),
            'passport_number': TextInput(attrs={
                'class': 'label_style',
                'placeholder': 'Номер паспорта'

            }),
            'date':TextInput(attrs={
                'class': 'label_style',
                'placeholder': 'Дата рождения'

            }),
            'adres': TextInput(attrs={
                'class': 'label_style',
                'placeholder': 'Адресс'

            }),

        }