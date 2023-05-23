import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
import re
from django.contrib.auth.models import User
from client.models import Client
from django.db import models
from books.models import Book


class ActGiveOut(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Читатель')
    today_date = models.DateField(auto_now_add=True)
    count_of_day = models.IntegerField(verbose_name='Дней использования', validators=[
        MinValueValidator(1, message='Минимальное количество дней составляет 1'),
        MaxValueValidator(30, message='Максимальное количество составляет 30')
    ])
    expected_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Предварительная цена', default=0.0)
    booksMustReturn = models.ManyToManyField(Book, verbose_name='Должен вернуть', related_name='booksMustReturn')
    booksGot = models.ManyToManyField(Book, verbose_name='Изначально взял', related_name='booksGot')
    status = models.TextField(null=True, blank=True)

    def diff_date_minus(self):
        diff = str(self.today_date - datetime.date.today())
        result = re.findall(r'\d', diff)
        return int(result[0])*-1

    def diff_date_plus(self):
        diff = str(self.today_date - datetime.date.today())
        result = re.findall(r'\d', diff)
        return int(result[0])



