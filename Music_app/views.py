from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, MusicFileForm
from .models import MusicFile

@login_required
def homepage(request):
    user = request.user
    music_files = MusicFile.objects.filter(access_type__in=['public', 'private', 'protected'])
    protected_files = music_files.filter(access_type='protected', allowed_emails__contains=user.email)
    context = {
        'user': user,
        'music_files': music_files,
        'protected_files': protected_files,
    }
    return render(request, 'Music_app/homepage.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('Music_app:login')
    else:
        form = RegistrationForm()
    return render(request, 'Music_app/registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'Music_app/registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            messages.success(request, 'File uploaded successfully.')
            return redirect('homepage')
    else:
        form = MusicFileForm()
    return render(request, 'Music_app/upload.html', {'form': form})
