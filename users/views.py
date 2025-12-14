from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from materials.serializers import CourseDetailSerializer
from users.models import Payment, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [
        DjangoFilterBackend,  # для filterset_fields
        filters.OrderingFilter,  # для ordering_fields
    ]
    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )
    search_fields = (
        "course",
        "lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)

class ManageSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')  # Получаем ID курса из тела запроса

        if not course_id:
            return Response(
                {"error": "course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем курс
        course = get_object_or_404(Course, id=course_id)

        # Ищем существующую подписку
        subscription = Subscription.objects.filter(
            user=user,
            course=course
        ).first()

        if subscription:
            # Если подписка есть — удаляем (или деактивируем)
            subscription.delete()  # Или subscription.is_active = False; subscription.save()
            message = "Подписка удалена"
            is_subscribed = False
        else:
            # Если подписки нет — создаём
            Subscription.objects.create(
                user=user,
                course=course,
                is_active=True
            )
            message = "Подписка добавлена"
            is_subscribed = True

        # Возвращаем данные курса с обновлённым флагом подписки
        serializer = CourseDetailSerializer(
            course,
            context={'request': request}
        )
        return Response({
            "message": message,
            "is_subscribed": is_subscribed,
            "course": serializer.data
        }, status=status.HTTP_200_OK)
