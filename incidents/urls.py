from django.urls import path
from . import views

app_name = 'incidents'  # <-- ¡Esta es la línea que faltaba y que causó el error!

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]