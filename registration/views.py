from django.shortcuts import render_to_response, get_list_or_404, redirect
from forms import RegistrationForm, BulletinRegistrationForm

def register(request):
    if request.method == 'POST':
        form = BulletinRegistrationForm(request.POST)
        if form.is_valid():
            ''' 
            We need to go to the email-sent page (even though an email
            isn't sent at the moment.
            '''
            form.save()
    else:
        form = BulletinRegistrationForm()
    return render_to_response('prototype/register.html', {'form': form,})
