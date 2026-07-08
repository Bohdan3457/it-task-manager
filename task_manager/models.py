from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    def __str__(self):
        return f"{self.username} ({self.position.name if self.position else 'No position'})"

class TaskType(models.Model):
    name = models.CharField(max_length=255),
    