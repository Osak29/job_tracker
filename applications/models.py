from django.db import models
from django.contrib.auth.models import User 
from datetime import date

class Application(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Envoyé'),
        ('relance', 'Relancé'),
        ('interview', 'Entretien'),
        ('refused', 'Refusé'),
        ('accepted', 'Accepté'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_applied = models.DateField()
    
    # AJOUTE BIEN CETTE LIGNE CI-DESSOUS :
    date_relance = models.DateField(blank=True, null=True) 

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    notes = models.TextField(blank=True)

    def doit_relancer(self):
        # On vérifie si la date de relance est vide (not self.date_relance)
        if self.status == 'sent' and not self.date_relance:
            diff = date.today() - self.date_applied
            return diff.days >= 7
        return False

    def __str__(self):
        return f"{self.company} - {self.position}"