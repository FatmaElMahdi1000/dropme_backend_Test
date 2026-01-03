from rest_framework import generics, permissions
from .serializers import DepositSerializer
from django.db.models import Sum
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Deposit, Wallet  # Added Wallet and RVM here

class DepositCreateView(generics.CreateAPIView):
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
                "total_points_earned": totals['total_points'] or 0,
                "wallet_status": "Active"
            })


class RegisterView(APIView):
    permission_classes = []  # Allow anyone to sign up
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Missing username or password"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the User
        user = User.objects.create_user(username=username, password=password)

            # Create the associated Wallet (Task 3 Requirement)
        Wallet.objects.create(user=user)

            # Create the Security Token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "message": "User and Wallet created successfully!"
            })
