from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('doing', 'En cours'),
        ('done', 'Terminé'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
