from django.shortcuts import render

from .models import Client
from .forms import UserForm

def authorization(request):
    form = UserForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

        else:
            context ={
                'form':form
            }
            return render(request, 'authorization.html', context)
    return render(request, 'authorization.html', context)


def list(request):
    clients = Client.objects.all()
    context = {
        'clients':clients
    }
    return render(request, 'clients.html', context)
