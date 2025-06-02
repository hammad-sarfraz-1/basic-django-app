from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import ProductViewSet, AdminCustomerViewSet

app_name = "store"

# API Routers
router = DefaultRouter()
router.register(r'api/products', ProductViewSet, basename='product')
router.register(r'api/admin/customers', AdminCustomerViewSet, basename='admin-customer')

urlpatterns = [
    # ----------------- Web Views -----------------
    # Customers
    path("customers/", views.customer_list_create, name="customer_list_create"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),

    # Products
    path("products/", views.ProductListCreateView.as_view(), name="product_list"),

    # Orders
    path("orders/", views.order_list_or_detail, name="order_list"),
    path("orders/new/", views.order_create, name="order_create"),
    path("orders/<int:pk>/", views.order_list_or_detail, name="order_detail"),

    # ----------------- API Endpoints -----------------
    # Public - Customers
    path("api/customers/", views.CustomerListAPI.as_view(), name="api_customer_list"),
    path("api/customers/<int:pk>/orders/", views.CustomerSpecificOrders.as_view(), name="api_customer_orders"),

    # Public - Orders
    path("api/orders/", views.OrderAPI.as_view(), name="api_order_list_create"),
    path("api/orders/<int:pk>/", views.OrderAPI.as_view(), name="api_order_detail_delete"),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ----------------- Include API Routers -----------------
    path("", include(router.urls)),
]
