from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import UserProfile
from .models import Incident
from .forms import IncidentForm

# 1. LISTAR (HOME)
@login_required
def home(request):
    incidents = Incident.objects.all()
    return render(request, 'incidents/home.html', {'incidents': incidents})

# 2. DETALLE
@login_required
def detail(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    return render(request, 'incidents/detail.html', {'incident': incident})

# 3. CREAR
@login_required
def create(request):
    form = IncidentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        incident = form.save(commit=False) # No lo guardes en la BD todavía
        incident.reported_by = request.user # Asigna el usuario actual
        incident.save() # Ahora sí, guárdalo
        return redirect('incidents:home')
    
    return render(request, 'incidents/create.html', {'form': form})

# 4. ACTUALIZAR (Solo Admins)
@login_required
def update(request, pk):
    # Verificamos si es administrador
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_admin():
        return HttpResponseForbidden('Only admins can edit incidents.')

    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        incident.title = request.POST.get('title', incident.title)
        incident.description = request.POST.get('description', incident.description)
        incident.severity = request.POST.get('severity', incident.severity)
        incident.save()
        return redirect('incidents:home')
        
    return render(request, 'incidents/update.html', {'incident': incident})

# 5. ELIMINAR (Solo Admins)
@login_required
def delete(request, pk):
    # Verificamos si es administrador
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_admin():
        return HttpResponseForbidden('Only admins can delete incidents.')

    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        incident.delete()
        return redirect('incidents:home')
        
    return render(request, 'incidents/confirm_delete.html', {'incident': incident})