from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        UserProfile.objects.create(
            user=user,
            role="Employee"
        )

        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)

        user = self.user

        # Superuser = Admin
        if user.is_superuser:

            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={"role": "Admin"}
            )

            if profile.role != "Admin":
                profile.role = "Admin"
                profile.save()

        else:

            # Normal Django user without profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={"role": "Employee"}
            )

        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": profile.role
        }

        return data