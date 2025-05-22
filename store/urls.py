from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Web Views - Customers
    path('customers/',           views.customer_list,             name='customer_list'),
    path('customers/new/',       views.customer_create,           name='customer_create'),
    path('customers/<int:pk>/',  views.customer_detail,           name='customer_detail'),

    # Web Views - Orders
    path('orders/',              views.order_list,                name='order_list'),
    path('orders/new/',          views.order_create,              name='order_create'),
    path('orders/<int:pk>/',     views.order_detail,              name='order_detail'),

    # API Endpoints
    path('api/customers/',             views.CustomerListAPI.as_view(),        name='api-customer-list'),
    path('api/customers/<int:pk>/orders/', views.CustomerOrdersAPI.as_view(),    name='api-customer-orders'),
    path('api/orders/',                views.OrderListCreateAPI.as_view(),     name='api-order-list-create'),
    path('api/orders/<int:pk>/',       views.OrderDetailDeleteAPI.as_view(),   name='api-order-detail-delete'),


    # Admin API for Customers
    path('api/admin/customers/',       views.AdminCustomerListCreateAPI.as_view(), name='api-admin-customer-list-create'),
    path('api/admin/customers/<int:pk>/', views.AdminCustomerDetailAPI.as_view(),     name='api-admin-customer-detail'),

]