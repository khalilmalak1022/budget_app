from django.db import models
from django.contrib.auth.models import User

class Objectif(models.Model):
    TYPE = [('epargne','Épargne'),('limite','Limite dépenses')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    montant_cible = models.DecimalField(max_digits=10, decimal_places=2)
    date_limite = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE)

    def __str__(self):
        return self.nom