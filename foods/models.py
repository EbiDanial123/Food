from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Categories=[
    ("BREAKFAST","Breakfast"),
     ("BIRIYANI","Biriyani"),
    ("PIZZA","Pizza"),
    ("BURGER","Burger"),
    ("DESSARTS","Dessarts"),
    ("BREVERAGES","Beverages")
]

sizechart=[
    ("REGULAR","Regular"),
    ("MEDIUM","Medium"),
    ("LARGE","Large"),
]

base=[
    ("MAIDA","Maida"),
    ("WHEAT","Wheat")
]
sauce=[
    ("RED CHILLI","Red chilli"),
    ("TOMATO","Tomato"),
    ("GREEN CHILLI","Green chilli")
]
toppings=[
    ("SWEETCORN","Sweetcorn"),
    ("PANEER","Paneer"),
    ("ONION","Onion"),
    ("CHEESE","Cheese"),
    ("OLIVE","Olive"),
    ("CAPSICUM","Capsicum"),
    ("CHICKEN","Chicken"),
    ('CHICKEN SALAMI','Chicken Salami'),
    ('CHICKEN SAUSAGE','Chicken Sausage'),
    ('BARBEQUE CHICKEN','Barbeque Chicken'),
    ('EGG','Egg'),
    ('LETTUCE','Lettuce')
]

class FoodItems(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField(null=True,blank=True)
    rating=models.FloatField(null=True,blank=True)
    foodpic = models.ImageField(upload_to='foodpic/', blank=True, null=True)
    Categories=models.CharField(max_length=100,choices=Categories)




class Sizechart(models.Model):
    size=models.CharField(max_length=100,choices=sizechart)
    size_in_cm=models.CharField(max_length=100)
    price=models.IntegerField()
    def __str__(self):
        return self.size

class Basetype(models.Model):
    basename=models.CharField(max_length=100,choices=base)
    base_img=models.ImageField(upload_to='base/', blank=True, null=True)
    def __str__(self):
        return self.basename

class Toppings(models.Model):
    name=models.CharField(max_length=100,choices=toppings)
    quantity=models.IntegerField()
    price=models.IntegerField()
    topping_img=models.ImageField(upload_to='topping/', blank=True, null=True)
    def __str__(self):
        return self.name

class Sauce(models.Model):
    sname=models.CharField(max_length=100,choices=sauce)
    price=models.IntegerField()
    sause_img=models.ImageField(upload_to='sauce/', blank=True, null=True)
    def __str__(self):
        return self.sname
    
class customizeoption(models.Model):
    food_type=models.CharField(max_length=100,choices=Categories)
    size= models.ForeignKey(Sizechart, related_name= 'sizecharts',on_delete=models.CASCADE)
    base= models.ForeignKey(Basetype,related_name= 'basetypes', on_delete=models.CASCADE)
    topping= models.ForeignKey(Toppings,related_name= 'toppings', on_delete=models.CASCADE)
    sauce= models.ForeignKey(Sauce,related_name= 'sauces', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.food_type}-{self.size}-{self.base}-{self.topping}-{self.sauce}"

from django.contrib.auth.models import User
from django.conf import settings
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    food_img = models.ImageField(upload_to='cart/', null=True, blank=True)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name

import uuid

import uuid
from django.db import models
from learnapp.models import UserDetails
class Order(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order_id)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    food_img = models.ImageField(upload_to='orders/', null=True, blank=True)

    def get_total(self):
        return self.price * self.quantity
