from rest_framework import generics, permissions
from .models import Deposit
from .serializers import DepositSerializer
from django.db.models import Sum
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class DepositCreateView(generics.CreateAPIView):
    # This View only handles creating new deposits
    queryset = Deposit.objects.all() #for new POST requests from the RVM
    serializer_class = DepositSerializer #Requests checked by this serializer
    # SECURITY
    # token based authentication part,RVM sends login req.>server sends back a token
    #> the RVM must use that token every time there's a request
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # This part ensures the 'user' field is automatically
        # set to the person who is currently logged in.
        serializer.save(user=self.request.user)

# The view
class UserSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_deposits = Deposit.objects.filter(user=user)

        totals = user_deposits.aggregate(
            total_weight=Sum('weight'),
            total_points=Sum('points_earned')
        )

        return Response({
            "username": user.username,
            "total_recycled_weight": totals['total_weight'] or 0,
            "total_points_earned": totals['total_points'] or 0
        })


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Send username and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "message": "User created successfully!"})
