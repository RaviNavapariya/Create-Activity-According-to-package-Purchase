from django.urls import path
from activity import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('create-package/', views.CreatePackageAPIView.as_view(), name='create-package'),
    path('create-activity/', views.CreateActivityAPIView.as_view(), name='create-activity'),
    path('all-activity/', views.GetAllActivityListAPIView.as_view(), name='all-activity'),
    path('purchase-package/', views.PurchasePackageAPIView.as_view(), name='purchase-package'),
]
