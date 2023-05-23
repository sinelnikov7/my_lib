from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelMultipleChoiceField

from .models import Genres, Authors


class Genre(forms.ModelForm):
    genre = forms.CharField(max_length=50, label='Жанр', error_messages={'unique':"Такой жанр уже добавлен"}, help_text='Введите имя жанра',
                            widget=forms.TextInput(attrs={'placeholder': 'Введите имя жанра'}))

    class Meta:
        model = Genres
        fields = '__all__'


class Author(forms.Form):
    firstName = forms.CharField(max_length=50, label='Имя')
    lastName = forms.CharField(max_length=50, label='Фамилия')
    foto = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Фотографии авторов')


class AddBook(forms.Form):
    name_r = forms.CharField(max_length=50, label='Название на русском')
    name_o = forms.CharField(max_length=50, label='Название на языке оригинала', required=False)
    price = forms.DecimalField(max_digits=6, decimal_places=2, label='Цена')
    count = forms.IntegerField(label='Кол-во доступных', validators=[
        MinValueValidator(0, message='Минимальное количество составляет 0'),
        MaxValueValidator(10, message='Максимальное количество составляет 10')
    ])
    price_for_day = forms.DecimalField(max_digits=6, decimal_places=2, label='Цена за день')
    year_of_made = forms.IntegerField(label='Год написания', max_value=2023, error_messages={'max_value':"Год не может быть больше текущего!!!!"}, validators=[
        MaxValueValidator(2022, message='Год не может быть больше текущего')
    ])
    count_of_pages = forms.IntegerField(label='Страниц в книге', validators=[
        MinValueValidator(1, message='Минимальное количество составляет 1')
    ])
    genres = ModelMultipleChoiceField(
        queryset=Genres.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите жанры'
    )
    authors = ModelMultipleChoiceField(
        queryset=Authors.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите авторов'
    )
    foto = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Фотографии книги')
