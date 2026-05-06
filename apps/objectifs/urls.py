from django.urls import path
from . import views

urlpatterns = [
    path('objectifs/', views.objectif_liste, name='objectif_liste'),
    path('objectifs/ajouter/', views.objectif_ajouter, name='objectif_ajouter'),
    path('objectifs/modifier/<int:pk>/', views.objectif_modifier, name='objectif_modifier'),
    path('objectifs/supprimer/<int:pk>/', views.objectif_supprimer, name='objectif_supprimer'),
]