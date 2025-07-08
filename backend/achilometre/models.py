from django.db import models
from django.contrib.auth.models import User

THEME_CHOICES = [
    ("work", "Travail"),
    ("personal", "Personnel"),
    ("urgent", "Urgent"),
    ("other", "Autre"),
]

THEME_COLORS = {
    "work": "#1E90FF",       # Bleu
    "personal": "#32CD32",   # Vert
    "urgent": "#FF4500",     # Rouge
    "other": "#808080",      # Gris
}


class Task(models.Model):

    @property
    def color(self):
        return THEME_COLORS.get(self.theme, "#3788d8")

    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('doing', 'En cours'),
        ('done', 'Terminé'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='todo')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default="other")

    def is_completed(self):
        return self.status == 'done'

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar_01.jpg')
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username