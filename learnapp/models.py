from django.db import models
from django.contrib.auth.models import User


user_type=[
    ("USER","user"),
    ("VENDOR","vendor")
]                                                                                                                                                                                                                                                     

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.BigIntegerField(null=True,blank=True)
    address = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.IntegerField()
    userpic = models.ImageField(upload_to='userpic/', blank=True, null=True)
    user_type=models.CharField(max_length=100,choices=user_type,default="user")

