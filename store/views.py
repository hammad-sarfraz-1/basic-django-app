# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

from .models import Customer, Order, Product
from django.views.generic.edit import CreateView
from .forms import CustomerForm, OrderForm
from .serializers import CustomerSerializer, OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics

# ------------------------------------------------------------------
# Traditional Django Views
# ------------------------------------------------------------------

def customer_list_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:customer_list_create')
    else:
        form = CustomerForm()

    customers = Customer.objects.order_by('-joined_on')
    return render(request, 'store/customer_list.html', {
        'customers': customers,
        'form': form
    })


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'store/customer_detail.html', {
        'customer': customer,
        'orders': customer.orders.all()
    })


def order_list_or_detail(request, pk=None):
    if pk is not None:
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'store/order_detail.html', {'order': order})
    
    orders = Order.objects.select_related('customer').order_by('-order_date')
    return render(request, 'store/order_list.html', {'orders': orders})


@csrf_exempt # no need for token, a security exemption
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:order_list_or_detail')
    else:
        form = OrderForm()
    return render(request, 'store/order_form.html', {'form': form})


# ------------------------------------------------------------------
# DRF API Views — Public APIs
# ------------------------------------------------------------------

class CustomerListOrOrdersAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        if pk:
            orders = Order.objects.filter(customer_id=pk).order_by('-order_date')
            serializer = OrderSerializer(orders, many=True)
        else:
            customers = Customer.objects.all().order_by('-joined_on')
            serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class OrderAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.select_related('customer').order_by('-order_date')
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({'detail': 'Order deleted'}, status=204)


# # Class -based view for Product
# class ProductListCreateAPI(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# ------------------------------------------------------------------
# DRF API Views — Admin-Only Endpoints
# ------------------------------------------------------------------

class AdminCustomerListCreateAPI(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-joined_on')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

class AdminCustomerDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

# ------------------------------------------------------------------
# Product Web views
# ------------------------------------------------------------------

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'store/product_list.html', {'products': products})

# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('store:product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'store/product_form.html', {'form': form})

# class ProductCreateView(CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'store/product_form.html'
#     success_url = reverse_lazy('product_add')
#     permission_classes = [AllowAny]

# class ProductCreateView(CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'store/product_form.html'
#     success_url = reverse_lazy('product_add')  # Redirect to same page after adding