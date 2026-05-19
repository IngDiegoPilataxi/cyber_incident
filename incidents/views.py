from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Incident
from django.contrib.auth.decorators import login_required 

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        title = request.POST.get('description', '').strip()
        description = request.POST.get('description', '').strip()

        
        if title and description:
            Incident.objects.create(
                title=title,
                description=description
            )
        return redirect('home')
    incidents = Incident.objects.all()
    return render(request, 'incidents/home.html', {'incidents': incidents})