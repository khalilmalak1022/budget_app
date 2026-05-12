from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_liste, name='transaction_liste'),
    path('transactions/ajouter/', views.transaction_ajouter, name='transaction_ajouter'),
    path('transactions/modifier/<int:pk>/', views.transaction_modifier, name='transaction_modifier'),
    path('transactions/supprimer/<int:pk>/', views.transaction_supprimer, name='transaction_supprimer'),
    path('categories/', views.categorie_liste, name='categorie_liste'),
    path('categories/ajouter/', views.categorie_ajouter, name='categorie_ajouter'),
    path('categories/modifier/<int:pk>/', views.categorie_modifier, name='categorie_modifier'),
    path('categories/supprimer/<int:pk>/', views.categorie_supprimer, name='categorie_supprimer'),
    path('historique/', views.historique, name='historique'),
]