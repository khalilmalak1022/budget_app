from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    devise = models.CharField(max_length=3, default='DH',
        choices=[('DH','Dirham'),('EUR','Euro'),('USD','Dollar')])

    def __str__(self):
        return f"Profil de {self.user.username}"

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

class Objectif(models.Model):
    TYPE = [('epargne','Épargne'),('limite','Limite dépenses')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    montant_cible = models.DecimalField(max_digits=10, decimal_places=2)
    date_limite = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE)

    def __str__(self):
        return self.nom

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    montant_limite = models.DecimalField(max_digits=10, decimal_places=2)
    periode = models.DateField()

    def __str__(self):
        return f"{self.categorie.nom} - {self.periode}"

class Notification(models.Model):
    TYPE = [('email','Email'),('alerte','Alerte')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE)
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} - {self.user.username}"