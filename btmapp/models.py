from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserRegisteration(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    
    phone = models.PositiveIntegerField()
    door_no = models.IntegerField()
    street = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    userpic = models.ImageField(upload_to="profiles/",blank=True, null=True)