from django.shortcuts import render_to_response, get_list_or_404, redirect
from session_proto.models import User, RegisterForm
import md5

def login(request):
    pass

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            # hash password
            hashpass = md5.new(password).hexdigest()
            # save model
            new_user = User(first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            password=hashpass)
            new_user.save()
            
            return redirect(login)
    else:
        form = RegisterForm()
    
    return render_to_response('prototype/register.html', {'form': form,})
