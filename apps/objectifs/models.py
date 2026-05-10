from django.db import models
from django.contrib.auth.models import User


class Objectif(models.Model):
    TYPE_CHOICES = [
        ('epargne', "Objectif d'épargne"),
        ('limite',  'Limite de dépenses'),
    ]

    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    nom           = models.CharField(max_length=200)
    type          = models.CharField(max_length=10, choices=TYPE_CHOICES, default='epargne')
    montant_cible = models.DecimalField(max_digits=12, decimal_places=2)
    date_limite   = models.DateField()
    description   = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_limite']

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"