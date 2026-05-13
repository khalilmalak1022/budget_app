from django.contrib import admin
from .models import Objectif

@admin.register(Objectif)
class ObjectifAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'type', 'montant_cible', 'date_limite', 'user')
    list_filter   = ('type', 'user')
    search_fields = ('nom',)