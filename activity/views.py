from django.shortcuts import render
from rest_framework.views import APIView
from activity.serializers import RegisterSerializer, LoginSerializer, PackageSerializer, PurchasePackageSerializer, ActivityCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Package, Activity, PurchasePackage
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'username':request.data.get('username'),
            'first_name':request.data.get('first_name'),
            'last_name':request.data.get('last_name'),
            'email':request.data.get('email'),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_data = User.objects.filter(email=email).first()
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=user_data, password=password)
            if user:
                login(request, user)
                token = RefreshToken.for_user(user)
                data = {
                    "user":user.email,
                    "refresh":str(token),
                    "access":str(token.access_token)
                }
                return Response(data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePackageAPIView(APIView):

    def get(self,request):
        data = Package.objects.all()
        serializer = PackageSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PackageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PurchasePackageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        id_name = Package.objects.filter(id=request.data['name']).values_list('name',flat=True)[0]
        serializer = PurchasePackageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        response_data = serializer.data
        data = {
            'message':f'You have purchased {id_name} Package',
            'Package name':id_name,
            'user':response_data['user']
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CreateActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        data = Activity.objects.filter(user=request.user)
        serializer = ActivityCreateSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        package = list(PurchasePackage.objects.filter(user=request.user).values_list('name__name',flat=True))
        if len(package) == 0:
            return Response({"message":f"You have no permission to create activity, please purchase package first!!!"},
            status=status.HTTP_400_BAD_REQUEST)
        else:
            count = 0
            for i in package:
                number_of_activity = Package.objects.filter(name=i).values_list('activity', flat=True)[0]
                count = count+number_of_activity
            total_activity = Activity.objects.filter(user=request.user).values_list('name',flat=True).count()
            if total_activity < count:            
                serializer = ActivityCreateSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":f"Your activity create limit is over, you have not created more than {total_activity} activities!"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllActivityListAPIView(APIView):

    def get(self, request):
        data = Activity.objects.all()
        serializer = ActivityCreateSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)