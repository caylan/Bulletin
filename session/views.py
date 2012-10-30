from django.shortcuts import render_to_response, get_list_or_404, redirect
from forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            '''
            If we have a valid form, then we create a user session.
            '''
            request.session['user'] = form.clean_user()
    form = LoginForm()
    return render_to_response('login.html', {'form' : form,})
