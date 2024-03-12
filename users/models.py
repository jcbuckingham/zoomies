from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # User's first name
    first_name = models.CharField(max_length=100)
    # User's last name
    last_name = models.CharField(max_length=100)
    # User's email address
    email = models.EmailField(unique=True)

    def __str__(self):
        # Returns full name, such as "Mary Poppins"
        return f"{self.first_name} {self.last_name}"

