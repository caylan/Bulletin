from django.shortcuts import render_to_response, get_list_or_404, redirect
from forms import RegistrationForm

def register(request):
    form = RegistrationForm()
    return render_to_response('prototype/register.html', {'form': form,})
