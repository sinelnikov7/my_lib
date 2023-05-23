import datetime
import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import ActGiveOutForm
from .models import ActGiveOut
from client.models import Client
from books.models import Book


@login_required
def take_book(request):
    form = ActGiveOutForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = ActGiveOutForm(request.POST)
        if form.is_valid():
            order = ActGiveOut()
            order.client = Client.objects.get(id=request.POST.get('client'))
            order.count_of_day = request.POST.get('count_of_day')
            books = request.POST.getlist('booksGot')
            price_count = 0
            # try:
            for i in books:
                book = Book.objects.get(id=i)
                price_count += book.price
            if len(books) >= 2 and len(books) < 4:
                price_count = float(price_count) * 0.1
            elif len(books) >= 4:
                price_count = float(price_count) * 0.15
            order.expected_price = price_count
            order.save()
            can_get = Client.objects.get(id=request.POST.get('client'))
            can_get.canGet = False
            can_get.save()
            for i in books:
                book = Book.objects.get(id=i)
                order.booksMustReturn.add(book.id)
                order.booksGot.add(book.id)
            for n in books:
                boo = Book.objects.get(id=n)
                count = book.count_now
                boo.count_now -= 1
                boo.save()
        else:
            context = {
                'form': form
            }
            return render(request, 'take_book.html', context)
    return render(request, 'take_book.html', context)

@login_required
def all_take(request):
    all_take = ActGiveOut.objects.all()
    context = {
        'all_take': all_take,
    }
    return render(request, 'all_take.html', context)


def search_take(request):
    all_take = ActGiveOut.objects.all()
    context = {
        'all_take': all_take,
    }
    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        try:
            client_id = Client.objects.get(name=firstName.title(), sur_name=lastName.title())
            all_take = ActGiveOut.objects.filter(Q(client_id=client_id.id))
            context = {
                'all_take': all_take,
            }
        except:
            context = {
                'not_found': 'Такие Имя и Фамилия не найдены',
            }
    return render(request, 'all_take.html', context)

@login_required
def order_edit(request, id):
    order = ActGiveOut.objects.get(id=id)
    must = len(order.booksMustReturn.all())
    if request.method == "POST":
        orders = request.POST.getlist("booksMustReturn")
        refund = len(orders)
        if must == refund:
            price = 0
            for book in order.booksMustReturn.all():
                count_day = int(re.findall(r'\d', str(order.today_date - datetime.date.today()))[0])
                price += (book.price_for_day * count_day)
            order.status = f'Читатель вернул все книги, общая итоговая сумма составила {price} мегарублей'
            order.save()
            client = Client.objects.get(id=order.client_id)
            client.canGet = True
            client.save()
            for i in orders:
                order.booksMustReturn.remove(i)
                get_book = Book.objects.get(id=i)
                get_book.count_now += 1
                get_book.save()
        else:
            price = 0
            for i in orders:
                order.booksMustReturn.remove(i)
                get_book = Book.objects.get(id=i)
                get_book.count_now += 1
                get_book.save()
                count_day = int(re.findall(r'\d', str(order.today_date - datetime.date.today()))[0])
                price += (get_book.price_for_day * count_day)
            elseBook = order.booksMustReturn.all()
            status = 'Читатель не вернул: '
            for i in elseBook:
                order.booksMustReturn.remove(i)
                get_book = Book.objects.get(id=i.id)
                get_book.count_now += 1
                get_book.save()
                price += get_book.price
                if i == elseBook[len(elseBook) - 1]:
                    status = f'{status} ' + f'{i}.'
                else:
                    status = f'{status} ' + f'{i},'
            status = f'{status} И итоговая сумма с учетом возмещения за не возвращенные книги составила - {price} мегарублей.'
            order.status = status
            order.save()
            client = Client.objects.get(id=order.client_id)
            client.canGet = True
            client.save()
    context = {
        'order': order,
    }
    return render(request, 'order_edit.html', context)
