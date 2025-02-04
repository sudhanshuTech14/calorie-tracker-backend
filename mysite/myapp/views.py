from rest_framework import generics, permissions
from .models import Food, Consume
from .serializers import FoodSerializer, ConsumeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import serializers

# List and create food items
class FoodListCreateView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]  # Change to IsAuthenticated if login is required

# Retrieve, update, or delete a specific food item
class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]

# List and create consumption records for authenticated users
# class ConsumeListCreateView(generics.ListCreateAPIView):
#     serializer_class = ConsumeSerializer
#     permission_classes = [IsAuthenticated]  # Requires authentication

#     def get_queryset(self):
#         return Consume.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         print(f"Authenticated user: {self.request.user}")
#         serializer.save(user=self.request.user)

class ConsumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ConsumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        selected_date = self.request.query_params.get('date', None)

        if selected_date:
            try:
                parsed_date = parsed_date(selected_date)  # Convert string to date object
                if parsed_date:
                    return Consume.objects.filter(user=user, date_consumed__date=parsed_date)
            except ValueError:
                return Consume.objects.filter(user=user)  # Default to all user's records if invalid date
        
        return Consume.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# API to get consumed food list for a specific date
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Consume
from .serializers import ConsumeSerializer

class ConsumeByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        selected_date = request.query_params.get('date', None)
        parsed_date = None  # Initialize before try block

        if not selected_date:
            return Response({"error": "Date parameter is required"}, status=400)

        try:
            parsed_date = parse_date(selected_date)  # Attempt to parse date
            if parsed_date is None:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

            # Filter consumed food by user and date
            consumed_foods = Consume.objects.filter(user=user, date_consumed__date=parsed_date)
            total_calories = sum(item.food_consumed.calories * item.quantity for item in consumed_foods)

            data = {
                "date": selected_date,
                "total_calories": total_calories,
                "consumed_foods": ConsumeSerializer(consumed_foods, many=True).data
            }

            return Response(data)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# Retrieve, update, or delete a consumption record
class ConsumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConsumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Consume.objects.filter(user=self.request.user)
    

# Registration Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

# Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View (JWT)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)    

#just making change.