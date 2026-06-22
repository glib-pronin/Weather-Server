from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

class EmailVerification(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='email_verification')
    code_hash = models.CharField(max_length=128, null=True)
    expires_at = models.DateTimeField(null=True)

    def set_code(self, code, ttl_minutes=15):
        self.code_hash = make_password(code)
        self.expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
        self.save()

    def is_expired(self):
        return timezone.now() >= self.expires_at
    
    def check_code(self, user_code):
        if self.code_hash and not self.is_expired():
            return check_password(user_code, self.code_hash)
        return False