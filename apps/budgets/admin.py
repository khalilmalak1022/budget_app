from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display  = ('categorie', 'montant_limite', 'periode', 'user')
    list_filter   = ('user', 'periode')
    search_fields = ('categorie__nom',)