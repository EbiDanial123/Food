from django.shortcuts import render,redirect,get_object_or_404
from foods.models import FoodItems,customizeoption,Cart,Order,OrderItem
from foods.forms import FoodForm,customizeoptionform
# Create your views here.
def food_details(request,id):
    fooditems=FoodItems.objects.get(id = id)
    return render(request,'foods/foodDetail.html',{'fooditems':fooditems})
def all_food(request):
    allfood=FoodItems.objects.all()
    return render(request,'foods/Allfoods.html',{'allfood':allfood})

def category_foods(request, category):
    foods = FoodItems.objects.filter(Categories=category)
    context = {
        'foods': foods,
        'category': category,
    }
    return render(request, 'foods/category.html', context)
 
def customize(request, id):
    food = customizeoption.objects.get(id=id)
    form=customizeoptionform()
    context={
        'food':food,
        'form':form
    }
    return render(request, 'foods/customize2.html',context)

def addfood(request):
    if request.method=='POST':
        form=FoodForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Allfoods')
    else:
        form = FoodForm()
    return render(request,'foods/addfood.html',{'form':form})

from django.shortcuts import get_object_or_404, redirect, render
from foods.models import FoodItems, Cart
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, FoodItems

def add_to_cart(request):

    if not request.user.is_authenticated:
        return redirect('login')

    food_id = request.POST.get('food_id')   # ✅ use POST (not GET)

    food = get_object_or_404(FoodItems, id=food_id)

    # Prevent duplicate items
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        name=food.name,
        defaults={
            'price': food.price,
            'food_img': food.foodpic,
            'quantity': 1
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def edit_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)

    if request.method == "POST":
        cart_item.quantity = request.POST.get('quantity')
        cart_item.save()
        return redirect('cart')   # cart page name

    return render(request, 'foods/edit_cart.html', {'item': cart_item})

def delete_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)

    if request.method == "POST":
        cart_item.delete()

    return redirect('cart')   # cart page name

from learnapp.models import UserDetails
from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    addfood = Cart.objects.all()   # or filter by user if you have auth

    total_price = sum(
        item.price * item.quantity
        for item in addfood
    )

    return render(request, 'foods/add_to_cart.html', {
        'addfood': addfood,
        'total_price': total_price
    })


def place_order(request):
    # if request.method == "POST":
    thing=Order.objects.all()
    foods=OrderItem.objects.all()
    return render(request,'foods/orderdetails.html',{'foods':foods,'thing':thing})

        # user = UserDetails.objects.get(id=request.session['user_id'])

        # cart_items = Cart.objects.filter(user=user)

        # if not cart_items:
        #     return redirect('Allfoods')

        # total = sum(item.price * item.quantity for item in cart_items)

        # Create Order
        # order = Order.objects.create(
        #     # user=user,
        #     total_price=total
        # )

        # Move items into OrderItem
        # for item in cart_items:
        #     OrderItem.objects.create(
        #         order=order,
        #         food_name=item.name,
        #         price=item.price,
        #         quantity=item.quantity,
        #         food_img=item.food_img
        #     )

        # # Clear Cart
        # cart_items.delete()

        # return redirect('order_details', order_id=order.order_id)
    
# def order_details(request, order_id):
#     order = get_object_or_404(Order, order_id=order_id)

#     return render(request, 'foods/orderdetails.html', {
#         'order': order,
#         'items': order.items.all()
#     })
