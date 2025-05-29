from django import forms

from .models import Customer, Order, Product


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone", "address"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ['customer', 'quantity', 'status']
        fields = ["customer", "product", "quantity", "status", "total_price"]
