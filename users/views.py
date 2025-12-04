from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [
        DjangoFilterBackend,  # для filterset_fields
        filters.OrderingFilter,  # для ordering_fields
    ]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    search_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)