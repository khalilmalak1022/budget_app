from django.db import models
from django.contrib.auth.models import User
from apps.transactions.models import Categorie

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    montant_limite = models.DecimalField(max_digits=10, decimal_places=2)
    periode = models.DateField()

    def __str__(self):
        return f"{self.categorie.nom} - {self.periode}"