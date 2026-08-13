from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    MealMate's custom user.
    A user is either a diner (customer) or a restaurant owner.
    Role decides which dashboard and permissions they get.
    """
    ROLE_CHOICES = (
        ('diner', 'Diner'),
        ('owner', 'Restaurant Owner'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='diner')
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_owner(self):
        return self.role == 'owner'

    def is_diner(self):
        return self.role == 'diner'

    def __str__(self):
        return f"{self.username} ({self.role})"
