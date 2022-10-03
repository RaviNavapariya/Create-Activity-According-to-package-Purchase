from django.contrib.auth.models import User
from rest_framework import serializers
from activity.models import Package, PurchasePackage, Activity


# Create your serializers here.


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id','name', 'price', 'activity']


class PurchasePackageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = PurchasePackage
        fields = ['name','user']


class ActivityCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Activity
        fields = ['id','name', 'user']