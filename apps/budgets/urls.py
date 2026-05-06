from django.urls import path
from . import views

urlpatterns = [
    path('budgets/', views.budget_liste, name='budget_liste'),
    path('budgets/ajouter/', views.budget_ajouter, name='budget_ajouter'),
    path('budgets/modifier/<int:pk>/', views.budget_modifier, name='budget_modifier'),
    path('budgets/supprimer/<int:pk>/', views.budget_supprimer, name='budget_supprimer'),
]