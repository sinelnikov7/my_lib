from django.urls import path

from .views import take_book, all_take, search_take, order_edit

app_name = 'take_return_book'

urlpatterns = [
    path('take_book/', take_book, name='take_book'),
    path('all_take/', all_take, name='all_take'),
    path('search_take/', search_take, name='search_take'),
    path('<int:id>/', order_edit, name='order_edit')
]
