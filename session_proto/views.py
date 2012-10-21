from django.shortcuts import render_to_response, get_list_or_404, redirect
from session_proto.models import User, RegisterForm, LoginForm
import md5
import session_manager

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # generate session
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashpass = md5.new(password).hexdigest()
            token = session_manager.login(email, hashpass)
            user = session_manager.getSession(token)
            response = render_to_response('prototype/login.html', {'user': user,})
            response.set_cookie('session_token', token)
            return response
    else:  # (TODO) get current session, if legit, show stuff, else, show login
        if 'session_token' in request.COOKIES:
            token = request.COOKIES['session_token']
            user = session_manager.getSession(token)
            return render_to_response('prototype/login.html', {'user': user,})
        form = LoginForm()
    return render_to_response('prototype/login.html', {'form': form,});

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
