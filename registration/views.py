from django.shortcuts import render_to_response, get_list_or_404, redirect
from forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            ''' 
            We need to go to the email-sent page (even though an email
            isn't sent at the moment.
            '''
            form.save()
            return render_to_response('email_sent.html', {'email': form.cleaned_data['email'] })
    else:
        form = RegistrationForm()
    return render_to_response('register.html', {'form': form,})

def confirm_email(request):
    pass
