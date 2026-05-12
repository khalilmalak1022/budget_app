from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    devise = models.CharField(max_length=3, default='DH',
        choices=[('DH','Dirham'),('EUR','Euro'),('USD','Dollar')])

    def __str__(self):
        return f"Profil de {self.user.username}"