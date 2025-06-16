from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .forms import CustomerForm, OrderForm, ProductForm
from .models import Customer, Order, Product
from .serializers import CustomerSerializer, OrderSerializer, ProductSerializer

# ------------------------------------------------------------------
# Traditional Django Views (Session-based)
# ------------------------------------------------------------------


def customer_list_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("store:customer_list_create")
    else:
        form = CustomerForm()

    customers = Customer.objects.order_by("-joined_on")
    return render(
        request, "store/customer_list.html", {"customers": customers, "form": form}
    )


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(
        request,
        "store/customer_detail.html",
        {"customer": customer, "orders": customer.orders.all()},
    )


def order_list_or_detail(request, pk=None):
    if pk is not None:
        order = get_object_or_404(Order, pk=pk)
        return render(request, "store/order_detail.html", {"order": order})

    orders = Order.objects.select_related("customer").order_by("-order_date")
    return render(request, "store/order_list.html", {"orders": orders})


@csrf_exempt
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("store:order_list")
    else:
        form = OrderForm()
    return render(request, "store/order_form.html", {"form": form})


# ------------------------------------------------------------------
# DRF API Views — JWT Required
# ------------------------------------------------------------------


# this function should only return the customers details
class CustomerListAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get(self, request, pk=None):

        customers = Customer.objects.all().order_by("id")
        serializer = self.serializer_class(customers, many=True)
        return Response(serializer.data)


class CustomerSpecificOrders(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, pk=None):
        customer = get_object_or_404(Customer, pk=pk)
        orders = customer.orders.all().order_by("-created_at")
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class OrderAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OrderSerializer

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            serializer = self.serializer_class(order)
        else:
            orders = Order.objects.select_related("customer").order_by("created_at")
            serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({"detail": "Order deleted"}, status=204)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# ------------------------------------------------------------------
# Admin-only endpoints (JWT Required)
# ------------------------------------------------------------------


class AdminCustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductListCreateView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        form = ProductForm()
        return render(
            request, "store/product_list.html", {"products": products, "form": form}
        )

    def post(self, request):
        if not request.user.is_staff:
            return redirect("store:product_list")  # Or raise permission denied

        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("store:product_list")

        products = Product.objects.all()
        return render(
            request, "store/product_list.html", {"products": products, "form": form}
        )
