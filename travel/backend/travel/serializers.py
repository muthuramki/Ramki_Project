from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TravelRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_admin"]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "is_admin"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TravelRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  

    # Convert date format to support 'YYYY-MM-DD' input
    start_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%d-%m-%Y"])
    return_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%d-%m-%Y"])

    class Meta:
        model = TravelRequest
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)
