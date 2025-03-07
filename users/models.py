from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('owner', 'Restaurant Owner'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    dietary_restrictions = models.TextField(
        blank=True, help_text="Comma-separated list of allergies (e.g., 'nuts,dairy')."
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
