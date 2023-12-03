from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrationForm

def buyer_account_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.role = 'Buyer'
            user.save()
            return HttpResponse('Registration successful!')
        else:
            # Form is not valid, render the form with errors
            print(form.errors)
            context = {'form': form}
            return render(request, 'account/buyer_register.html', context)
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'account/buyer_register.html', context)

def seller_account_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.role = 'Seller'
            user.save()
            return HttpResponse('Registration successful!')
        else:
            print(form.errors)
            # Form is not valid, render the form with errors
            context = {'form': form}
            return render(request, 'account/seller_register.html', context)
    else:
        form = RegistrationForm()
        print('-----------------')
        context = {'form': form}
        return render(request, 'account/seller_register.html', context)
