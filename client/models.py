from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя")
    sur_name = models.CharField(max_length=30, verbose_name="Фамилия")
    last_name = models.CharField(max_length=30, verbose_name="Отчество")
    passport_number = models.CharField(max_length=40, blank=True, unique=True, verbose_name="Номер паспорта")
    date = models.DateField(verbose_name="Дата рождения")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    adres = models.CharField(max_length=40, verbose_name="Адресс")
    canGet = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.sur_name

    class Meta:
        verbose_name_plural = "Читатели"
        verbose_name = "Читатель"