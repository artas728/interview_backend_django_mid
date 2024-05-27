from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.is_active = False
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListByDateView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        embargo_date = request.query_params.get('embargo_date')

        if not start_date or not embargo_date:
            return Response(
                {"error": "start_date and embargo_date query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        orders = Order.objects.filter(
            Q(start_date__gte=start_date) & Q(embargo_date__lte=embargo_date)
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)