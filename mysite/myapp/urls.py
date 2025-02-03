from django.urls import path
from .views import FoodListCreateView, FoodDetailView, ConsumeListCreateView, ConsumeDetailView
from .views import RegisterView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('foods/', FoodListCreateView.as_view(), name='food-list-create'),
    path('foods/<int:pk>/', FoodDetailView.as_view(), name='food-detail'),
    path('consume/', ConsumeListCreateView.as_view(), name='consume-list-create'),
    path('consume/<int:pk>/', ConsumeDetailView.as_view(), name='consume-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
