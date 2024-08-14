from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('author', 'Author'),
        ('user', 'User'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.jpg')

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

