from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    couleur = models.CharField(max_length=7, default='#3498db')
    icone = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class Transaction(models.Model):
    TYPE = [('depense','Dépense'),('revenu','Revenu')]
    FREQUENCE = [
        ('journalier','Journalier'),
        ('mensuel','Mensuel'),
        ('hebdo','Hebdomadaire'),
        ('annuel','Annuel'),
        ('variable','Variable'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    est_recurrente = models.BooleanField(default=False)
    frequence = models.CharField(max_length=10,
        choices=FREQUENCE, null=True, blank=True)

    def __str__(self):
        return self.description