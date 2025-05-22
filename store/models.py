from django.db import models

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, blank=True)
    address    = models.CharField(max_length=255, blank=True)
    joined_on  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
    ]

    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date  = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} for {self.customer}"
