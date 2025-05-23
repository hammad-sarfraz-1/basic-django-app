from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Customer, Order
from .forms import CustomerForm, OrderForm
from .serializers import CustomerSerializer, OrderSerializer

from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

# ------------------------------------------------------------------
# Traditional Django Views
# ------------------------------------------------------------------

# List all customers (HTML)
def customer_list(request):
    customers = Customer.objects.order_by('-joined_on')
    return render(request, 'store/customer_list.html', {'customers': customers})

# Detail view of one customer + their orders (HTML)
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'store/customer_detail.html', {
        'customer': customer,
        'orders': customer.orders.all()
    })

# Create a new customer (HTML)
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'store/customer_form.html', {'form': form})

# List all orders (HTML)
def order_list(request):
    orders = Order.objects.select_related('customer').order_by('-order_date')
    return render(request, 'store/order_list.html', {'orders': orders})

# Detail view of one order (HTML)
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_detail.html', {'order': order})

# Create a new order (HTML)
@csrf_exempt
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:order_list')
    else:
        form = OrderForm()
    return render(request, 'store/order_form.html', {'form': form})


# ------------------------------------------------------------------
# DRF API Views — Public APIs
# ------------------------------------------------------------------

# 1. List all customers (API)
class CustomerListAPI(generics.ListAPIView):
    queryset = Customer.objects.all().order_by('-joined_on')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

# 2. List orders for a single customer (API)
class CustomerOrdersAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        customer_id = self.kwargs['pk']
        return Order.objects.filter(customer_id=customer_id).order_by('-order_date')

# 3. List all orders & create new order (API)
class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

# 4. Retrieve & delete a single order (API)
class OrderDetailDeleteAPI(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


# ------------------------------------------------------------------
# DRF API Views — Admin-Only Endpoints
# ------------------------------------------------------------------

# Admin: list & create customers
class AdminCustomerListCreateAPI(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-joined_on')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

# Admin: retrieve, update, delete a customer
class AdminCustomerDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
