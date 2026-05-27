from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import UserProfile
from incidents.models import Incident

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # Creamos el usuario base de Django
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'], # Usamos password1 del formulario
        )
        # Creamos el perfil asociado con el rol elegido
        UserProfile.objects.create(
            user=user,
            role=form.cleaned_data['role']
        )
        login(request, user) # Logueamos al usuario automáticamente tras registrarse
        return redirect('incidents:home')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        # authenticate verifica que el usuario y la contraseña sean correctos
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            # Redirige a donde quería ir, o por defecto a home
            return redirect(request.GET.get('next', 'incidents:home'))
        error = 'Invalid credentials. Try again.'
    return render(request, 'accounts/login.html', {'error': error})

def logout_view(request):
    # Por seguridad, el logout solo se acepta mediante el método POST
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return redirect('incidents:home')

@login_required
def dashboard_view(request):
    # Obtenemos el perfil y los incidentes que reportó este usuario
    profile = UserProfile.objects.get(user=request.user)
    incidents = Incident.objects.filter(reported_by=request.user)
    
    return render(request, 'accounts/dashboard.html', {
        'profile': profile,
        'incidents': incidents,
    })