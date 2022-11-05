from datetime import datetime

from django.db import models

from authentication.models import User


# Create your models here.
class Tickets(models.Model):
    topic = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.now())
    STATUS_SELECTION = (
        ('r', 'Resolved'),
        ('u', 'Unsolved'),
        ('F', 'Freeze')
    )
    status = models.CharField(max_length=1, choices=STATUS_SELECTION, blank=True, default='u')
    idUser = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic


class TicketsAnswer(models.Model):
    answer = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.now())
    idAdmin = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    idTickets = models.ForeignKey(Tickets, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
