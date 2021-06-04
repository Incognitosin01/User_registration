from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User,AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

  contact = PhoneNumberField()

  class Meta:
    ordering = ['first_name','last_name','email',]

  # def __str__(self):
  #   return f"{self.CustomUser.get_full_name()}"

class Application(models.Model):

  F_key = models.ForeignKey(CustomUser,default=None,on_delete=models.CASCADE, unique=True)
  address = models.TextField(max_length=250)
  resume = models.FileField()
  aadhar = models.FileField()
  Marksheet = models.FileField()

  # def _str_(self):
  #   return f"{self.CustomUser.get_full_name()}"
