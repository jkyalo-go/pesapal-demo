import datetime

from django.shortcuts import render
from django import views
from django.http import JsonResponse, HttpResponse

from webapp.forms import UserForm


# Create your views here.
def home_view(request):
    # Instantiate a dictionary for context to be rendered with html
    context = dict()
    if request.method == 'GET':
        context = {'donor_form': UserForm()}
    elif request.method == 'POST':
        donor_form = UserForm(data=request.POST)
        if donor_form.is_valid():
            print(donor_form.cleaned_data)
            return HttpResponse('Donation successful Thank you.')
        else:
            print('invalid')
            print(donor_form.errors)
            context = {'donor_form': UserForm(data=donor_form.data)}
    return render(request, 'webapp/home.html', context, 'text/html', 200)
