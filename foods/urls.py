from django.urls import path
from foods import views
urlpatterns = [
    path('', views.all_food, name='Allfoods'),
    path('foods/<int:id>/', views.food_details, name='foodDetail'),
    path('category/<str:category>/', views.category_foods, name='category_foods'),
    path('customize/<int:id>/', views.customize, name='customize'),
    path('addfood/',views.addfood,name='addfood'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_cart'),
    path('cart/edit/<int:id>/', views.edit_cart, name='edit_cart'),
    path('cart/delete/<int:id>/', views.delete_cart, name='delete_cart'),
    path('place-order/', views.place_order, name='place_order'),
    # path('order/<uuid:order_id>/', views.order_details, name='order_details'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('payment-options/<int:order_id>/', views.payment_options, name='payment_options'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('thank-you/<int:order_id>/', views.final_thankyou, name='final_thankyou'),





    ]