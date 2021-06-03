from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.

class Application(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  contact = PhoneNumberField()
  address = models.TextField(max_length=250)

  resume = models.FileField()
  aadhar = models.FileField()
  Marksheet = models.FileField()

  def __str__(self):
    return f"{self.user.get_full_name()}"
