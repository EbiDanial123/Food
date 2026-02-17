from django import forms
from foods.models import FoodItems,customizeoption,Cart

class FoodForm(forms.ModelForm):
    class Meta:
        model=FoodItems
        fields=['name','price','rating','foodpic','Categories']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'rating':forms.NumberInput(attrs={'class':'form-control','step':'0.1'}),
            'Categories':forms.Select(attrs={'class':'form-control'}),
        }
class customizeoptionform(forms.ModelForm):
    class Meta:
        model=customizeoption
        fields=['food_type','size','base','topping','sauce']  
        
class cartform(forms.ModelForm): 
    class Meta:
        model=Cart
        fields="__all__"
                                                                                                                                                                                                                                                                                                                                                                                                                 