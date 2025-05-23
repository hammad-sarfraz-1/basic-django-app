from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Web Views - Customers
    path('customers/',           views.customer_list,             name='customer_list'),        # GET
    path('customers/new/',       views.customer_create,           name='customer_create'),      # GET (form), POST (submit)
    path('customers/<int:pk>/',  views.customer_detail,           name='customer_detail'),      # GET

    # Web Views - Orders
    path('orders/',              views.order_list,                name='order_list'),           # GET 
    path('orders/new/',          views.order_create,              name='order_create'),         # GET (form), POST (submit)
    path('orders/<int:pk>/',     views.order_detail,              name='order_detail'),         # GET

    # API Endpoints
    path('api/customers/',             views.CustomerListAPI.as_view(),        name='api-customer-list'),           # GET done
    path('api/customers/<int:pk>/orders/', views.CustomerOrdersAPI.as_view(),    name='api-customer-orders'),       # GET done
    path('api/orders/',                views.OrderListCreateAPI.as_view(),     name='api-order-list-create'),       # GET done, POST done
    path('api/orders/<int:pk>/',       views.OrderDetailDeleteAPI.as_view(),   name='api-order-detail-delete'),     # GET done, DELETE done

    # Admin API for Customers
    path('api/admin/customers/',       views.AdminCustomerListCreateAPI.as_view(), name='api-admin-customer-list-create'),  # GET done, POST done
    path('api/admin/customers/<int:pk>/', views.AdminCustomerDetailAPI.as_view(),     name='api-admin-customer-detail'),     # GET done, PATCH done, DELETE done

]