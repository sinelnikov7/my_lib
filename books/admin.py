from django.contrib import admin

from .models import Genres, Authors, FotosAuthor, Book, FotoBook

admin.site.register(Genres)
admin.site.register(Authors)
admin.site.register(FotosAuthor)
admin.site.register(Book)
admin.site.register(FotoBook)
# Register your models here.
