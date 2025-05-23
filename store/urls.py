# urls.py
from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    # Web Views - Customers
    path('customers/',                  views.customer_list_create, name='customer_list_create'),           
    path('customers/<int:pk>/',         views.customer_detail, name='customer_detail'),
    # Web Views - Products
    # path('products/',            views.product_list,    name='product_list'),
    # path('products/new/',        views.product_create,  name='product_create'),


    # Web Views - Orders
    path('orders/',                     views.order_list_or_detail, name='order_list'),
    path('orders/new/',                 views.order_create, name='order_create'),
    path('orders/<int:pk>/',            views.order_list_or_detail, name='order_detail'),

    # API Endpoints - Public
    path('api/customers/',                  views.CustomerListOrOrdersAPI.as_view(), name='api_customer_list'), # Done
    path('api/customers/<int:pk>/orders/',  views.CustomerListOrOrdersAPI.as_view(), name='api_customer_orders'),
    path('api/orders/',                     views.OrderAPI.as_view(), name='api_order_list_create'),
    path('api/orders/<int:pk>/',            views.OrderAPI.as_view(), name='api_order_detail_delete'),

    # API Endpoints - Products

    # path('api/products/',               views.ProductListCreateAPI.as_view(), name='api-product-list-create'),
    # path('api/products/<int:pk>/',      views.ProductDetailAPI.as_view(), name='api-product-detail'),

    # path('admin/add-product/', ProductCreateView.as_view(), name='product_add'),




    # API Endpoints - Admin
    path('api/admin/customers/',            views.AdminCustomerListCreateAPI.as_view(), name='api_admin_customer_list_create'),
    path('api/admin/customers/<int:pk>/',   views.AdminCustomerDetailAPI.as_view(), name='api_admin_customer_detail'),
]
