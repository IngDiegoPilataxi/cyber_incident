from django.contrib import admin
from .models import Incident


# Register your models here.

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'reported_at')
    search_fields = ('title', 'description')
    list_filter = ('reported_at',)