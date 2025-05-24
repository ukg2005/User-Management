from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.conf import settings

def signup(request):
    user_type = request.GET.get('user_type')
    if not user_type or user_type not in ['patient', 'doctor']:
        return redirect('landing')

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = user_type
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            return redirect('dashboard')
    else:
        form = SignupForm(initial={'user_type': user_type})
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': user_type})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user_type = request.POST.get('user_type')
        if not user_type or user_type not in ['patient', 'doctor']:
            return redirect('landing')
         
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            user = authenticate(request, username=username, password=password, user_type=user_type)
            if user is not None:
                login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                return redirect('dashboard')
            form.add_error(None, 'Invalid username or password for this user type.')
        login_error = form.errors.get('__all__')
    else:
        user_type = request.GET.get('user_type')
        if not user_type or user_type not in ['patient', 'doctor']:
            return redirect('landing')
        form = LoginForm(initial={'user_type': user_type})
        login_error = None
    return render(request, 'accounts/login.html', {'form': form, 'user_type': user_type, 'login_error': login_error})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('landing')

def landing_page(request):
    return render(request, 'accounts/landing_page.html')