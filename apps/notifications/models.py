from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    TYPE = [('email','Email'),('alerte','Alerte')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE)
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} - {self.user.username}"