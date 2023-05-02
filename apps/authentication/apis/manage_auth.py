from uuid import UUID
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

# Permission
from rest_framework.permissions import IsAuthenticated

# Custom Permission Classes\
from apps.common.permissions import AddUser

# Access Token
from apps.auth_token.models import AccessToken
from apps.auth_token.service import create_token

# Views
from rest_framework import generics
from rest_framework.views import APIView
# Models
from apps.user.models import User

# Permission Classes
from apps.user.permissions import OwnProfilePermission


# Serilizers Classes
from apps.authentication.serilizers import SignUpSerializer
from apps.authentication.serilizers import LoginSerializer
from apps.authentication.serilizers import ChangePasswordSerializer

class Login(APIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)


class Register(generics.CreateAPIView):

    """
    API endpoint to register a new user.
    """
    
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'message': 'User registered successfully.',
            'data': response.data
        }, status=response.status_code)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_token = request.auth.decode()
        obj = AccessToken.objects.get(token=UUID(hex=access_token))
        obj.validity = AccessToken.TokenValidity.INVALID
        obj.save()
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)


class Refresh(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        access_token = request.auth.decode()
        obj = AccessToken.objects.get(token=UUID(hex=access_token))
        obj.validity = AccessToken.TokenValidity.INVALID
        obj.save()

        access_token = create_token(request.user)
        return Response({"access_token": access_token})

class ChangePassword(APIView):
    """
    API endpoint for changing a user's password.
    """
    permission_classes = (IsAuthenticated,OwnProfilePermission)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)