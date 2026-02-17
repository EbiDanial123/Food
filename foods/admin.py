from django.contrib import admin
from foods.models import FoodItems,Sizechart,Basetype,Toppings,Sauce,customizeoption,Cart

# Register your models here.
admin.site.register(FoodItems)
admin.site.register(Cart)
admin.site.register(Sizechart)
admin.site.register(Basetype)
admin.site.register(Toppings)
admin.site.register(Sauce)
admin.site.register(customizeoption)
