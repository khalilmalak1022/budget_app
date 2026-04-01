from django.contrib import admin
from .models import Profil, Categorie, Transaction, Objectif, Budget, Notification

admin.site.register(Profil)
admin.site.register(Categorie)
admin.site.register(Transaction)
admin.site.register(Objectif)
admin.site.register(Budget)
admin.site.register(Notification)