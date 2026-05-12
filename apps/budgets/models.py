from django.db import models
from django.contrib.auth.models import User
from apps.transactions.models import Categorie


class Budget(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie      = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    montant_limite = models.DecimalField(max_digits=12, decimal_places=2)
    periode        = models.DateField()  # 1er jour du mois concerné
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['-periode']
        unique_together = ('user', 'categorie', 'periode')

    def __str__(self):
        return f"Budget {self.categorie.nom} — {self.periode.strftime('%m/%Y')}"