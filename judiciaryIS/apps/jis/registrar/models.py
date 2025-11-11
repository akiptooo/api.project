from django.db import models
from django.contrib.auth.models import User

class Registrar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registrar_profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
