from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, Subscription, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "payment_method",
            "payment_link",
        ]
        read_only_fields = ["user", "payment_date", "payment_link"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "course",
            "user_email",
            "course_name",
            "created_at",
            "is_active",
        ]
        read_only_fields = ["created_at"]
