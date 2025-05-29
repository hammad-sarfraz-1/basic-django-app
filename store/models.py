from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=12, blank=True)
    address    = models.CharField(max_length=255, blank=True)
    joined_on  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField()


    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
    ]

    customer    = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orders')  # cascade -> if customer is deleted, all orders are deleted
    product     = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orders') #protect-> if product is deleted then order will not be deleted
    
    quantity    = models.PositiveIntegerField(default=1)
    status      = models.CharField(max_length=1,choices=STATUS_CHOICES,default='P')
    
    total_price = models.DecimalField(max_digits=12,decimal_places=2,default=0.00  # <-- give a default so existing rows migrate cleanly
                                      )
    created_at  = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total_price on every save
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} – {self.product.name} x{self.quantity}"
