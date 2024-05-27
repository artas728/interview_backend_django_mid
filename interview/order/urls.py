
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView, OrderListByDateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('deactivate/<int:pk>/', DeactivateOrderView.as_view(), name='deactivate-order'),
    path('filter-by-date/', OrderListByDateView.as_view(), name='order-list-by-date'),
]