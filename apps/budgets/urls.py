from django.urls import path
from . import views

urlpatterns = [
    path('budgets/',                    views.budget_liste,     name='budget_liste'),
    path('budgets/ajouter/',            views.budget_ajouter,   name='budget_ajouter'),
    path('budgets/<int:pk>/modifier/',  views.budget_modifier,  name='budget_modifier'),
    path('budgets/<int:pk>/supprimer/', views.budget_supprimer, name='budget_supprimer'),
]