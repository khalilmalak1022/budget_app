from django.urls import path
from budget import views

urlpatterns = [
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profil/', views.profil, name='profil'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Transactions
    path('transactions/', views.transaction_liste, name='transaction_liste'),
    path('transactions/ajouter/', views.transaction_ajouter, name='transaction_ajouter'),
    path('transactions/modifier/<int:pk>/', views.transaction_modifier, name='transaction_modifier'),
    path('transactions/supprimer/<int:pk>/', views.transaction_supprimer, name='transaction_supprimer'),

    # Catégories
    path('categories/', views.categorie_liste, name='categorie_liste'),
    path('categories/ajouter/', views.categorie_ajouter, name='categorie_ajouter'),
    path('categories/modifier/<int:pk>/', views.categorie_modifier, name='categorie_modifier'),
    path('categories/supprimer/<int:pk>/', views.categorie_supprimer, name='categorie_supprimer'),

    # Historique
    path('historique/', views.historique, name='historique'),

    # Objectifs
    path('objectifs/', views.objectif_liste, name='objectif_liste'),
    path('objectifs/ajouter/', views.objectif_ajouter, name='objectif_ajouter'),
    path('objectifs/modifier/<int:pk>/', views.objectif_modifier, name='objectif_modifier'),
    path('objectifs/supprimer/<int:pk>/', views.objectif_supprimer, name='objectif_supprimer'),

    # Budgets
    path('budgets/', views.budget_liste, name='budget_liste'),
    path('budgets/ajouter/', views.budget_ajouter, name='budget_ajouter'),
    path('budgets/modifier/<int:pk>/', views.budget_modifier, name='budget_modifier'),
    path('budgets/supprimer/<int:pk>/', views.budget_supprimer, name='budget_supprimer'),

    # Export
    path('export/', views.export_excel, name='export_excel'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),

    # Chatbot
    path('chatbot/', views.chatbot, name='chatbot'),
]