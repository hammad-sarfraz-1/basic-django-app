from django.shortcuts    import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms              import SignUpForm, LoginForm

# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  
            # auto-login:
            username=form.cleaned_data['username']
            pwd=form.cleaned_data['password1']
            user=authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('/')
    else:
        form=SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    logout(request)
    return redirect('/accounts/login')

@login_required

def home_view(request):
    return render(request, 'home.html',{'user': request.user})

