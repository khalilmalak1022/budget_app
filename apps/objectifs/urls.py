from django.urls import path
from . import views

urlpatterns = [
    path('objectifs/',                    views.objectif_liste,     name='objectif_liste'),
    path('objectifs/ajouter/',            views.objectif_ajouter,   name='objectif_ajouter'),
    path('objectifs/<int:pk>/modifier/',  views.objectif_modifier,  name='objectif_modifier'),
    path('objectifs/<int:pk>/supprimer/', views.objectif_supprimer, name='objectif_supprimer'),
]