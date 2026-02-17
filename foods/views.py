from django.shortcuts import render,redirect,get_object_or_404
from foods.models import FoodItems,customizeoption,Cart,Order,OrderItem,Toppings
from foods.forms import FoodForm,customizeoptionform,CustomizeForm
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
    food = get_object_or_404(FoodItems, id=id)

    if request.method == "POST":
        form = CustomizeForm(request.POST)
        form.fields['topping'].queryset = Toppings.objects.filter(
            category=food.Categories
        )

        if form.is_valid():
            size = form.cleaned_data['size']
            base = form.cleaned_data['base']
            sauce = form.cleaned_data['sauce']
            toppings = form.cleaned_data['topping']

            base_price = food.price
            size_price = size.price
            sauce_price = sauce.price
            topping_total = sum(t.price for t in toppings)

            final_price = base_price + size_price + sauce_price + topping_total

            Cart.objects.create(
                user=request.user,
                name=food.name,
                price=final_price,
                quantity=1,
                food_img=food.foodpic
            )

            return redirect('cart')   # 🔥 THIS MUST EXIST

        else:
            print(form.errors)

    else:
        form = CustomizeForm()
        form.fields['topping'].queryset = Toppings.objects.filter(
            category=food.Categories
        )

    return render(request, 'foods/customize2.html', {
        'form': form,
        'food': food
    })

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

from django.shortcuts import redirect, render, get_object_or_404
from .models import Order, OrderItem, Cart

from django.shortcuts import redirect

def place_order(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cart')

        total_price = sum(item.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_name=item.name,
                price=item.price,
                quantity=item.quantity,
                food_img=item.food_img
            )

        cart_items.delete()

        # ✅ Redirect to payment page
        return redirect('payment_page', order_id=order.id)
from django.shortcuts import render, get_object_or_404

def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()


    return render(request, 'foods/orderdetails.html', {
        'order': order,
        'thing': items
    })

def payment_options(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        method = request.POST.get('payment_method')

        order.payment_method = method
        order.payment_status = "Paid"  # Dummy success
        order.save()

        return redirect('payment_success', order_id=order.id)

    return render(request, 'foods/payment_options.html', {'order': order})



def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'foods/payment_success.html', {'order': order})

def final_thankyou(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'foods/thank_you.html', {'order': order})
