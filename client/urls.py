from django.urls import path

from .views import authorization, list

app_name = 'client'

urlpatterns =[
    path('', authorization, name='authorization'),
    path('client/', list, name='list')
]