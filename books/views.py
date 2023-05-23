from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .forms import Genre, Author, AddBook
from .models import Genres, Authors, FotosAuthor, Book, FotoBook


# Добовление жанра
@login_required
def add_genres(request):

    form = Genre()
    allGenres = Genres.objects.all()
    context = {
        'form': form,
        'allGenres': allGenres,
    }
    if request.method == 'POST':

        form = Genre(request.POST)
        if form.is_valid():
            form.save()
        else:
            allGenres = Genres.objects.all()
            context = {
                'form': form,
                'allGenres': allGenres,
            }
            return render(request, 'add_genres.html', context)
    return render(request, 'add_genres.html', context)


@login_required
def add_authors(request):
    formAuthors = Author()
    author = Authors.objects.all()
    foto = FotosAuthor.objects.all()
    context = {
        'formAuthors': formAuthors,
        'author': author,
        'foto': foto,
    }
    if request.method == 'POST':
        images = request.FILES.getlist('foto')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        autor = Authors()
        autor.lastName = lastName
        autor.firstName = firstName
        autor.save()
        pk = autor.pk
        for i in images:
            authors = Authors.objects.get(pk=pk)
            FotosAuthor.objects.create(foto=i, authors=authors)
    return render(request, 'add_authors.html', context)

@login_required
def add_book(request):
    form = AddBook()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = AddBook(request.POST, request.FILES)
        if form.is_valid():
            new_book = Book()
            new_book.name_r = request.POST.get('name_r')
            new_book.name_o = request.POST.get('name_o')
            new_book.price = request.POST.get('price')
            new_book.count = request.POST.get('count')
            new_book.price_for_day = request.POST.get('price_for_day')
            new_book.year_of_made = request.POST.get('year_of_made')
            new_book.count_of_pages = request.POST.get('count_of_pages')
            genres = request.POST.getlist('genres')
            authors = request.POST.getlist('authors')
            images = request.FILES.getlist('foto')
            new_book.save()
            pk = new_book.pk
            for i in genres:
                genre = Genres.objects.get(id=i)
                new_book.genres.add(genre.id)
            for n in authors:
                author = Authors.objects.get(id=n)
                new_book.authors.add(author.id)

            for image in images:
                book = Book.objects.get(pk=pk)
                FotoBook.objects.create(foto=image, book=book)
        else:
            context = {
                'form': form,
            }
            return render(request, 'add_book.html', context)
    return render(request, 'add_book.html', context)

def get_book(request):
    if request.method == "GET":
        getBook = request.GET.get('book')
        books = Book.objects.filter(Q(name_r__contains=getBook.title()))
        context = {
            'books': books,
        }
    return render(request, 'book.html', context)

def book_detail(request, id):
    book = Book.objects.get(id=id)
    context = {
        'book': book,
    }
    return render(request, 'book_detail.html', context)


def book(request):
    books = Book.objects.prefetch_related('genres').all()
    context = {
        'books': books,
    }
    return render(request, 'book.html', context)