from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrationForm

def account_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponse('Registration successful!')
        else:
            # Form is not valid, render the form with errors
            context = {'form': form}
            return render(request, 'account/register.html', context)
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)
