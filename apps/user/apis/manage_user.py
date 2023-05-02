from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

#Generics Views
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView

# Permission Classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

# Custom Permission Classes
from apps.common.permissions import AddUser
from apps.common.permissions import ChangeUser
from apps.common.permissions import ViewUser
from apps.common.permissions import DeleteUser

# Serializers Classes
from apps.user.serializers import AddUserSerializer
from apps.user.serializers import UpdateDetailUserSerializer
from apps.user.serializers import UserListSrializer

# Selectors
from apps.user.selectors import user_list

# Pagination 
from apps.api.paginations import (
    LimitOffsetPagination,
    get_paginated_response,
)

# Filter 
from apps.user.filters import UserFilter

# Models
from apps.user.models import User


# Admin add user api view
class AddUser(CreateAPIView):
    """
    API endpoint to add a new user.
    """
    permission_classes = (IsAuthenticated, AddUser)
    serializer_class = AddUserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'message': 'User Added successfully.',
            'data': response.data
        }, status=response.status_code)


# Admin update user api view
class UpdateUser(UpdateAPIView):
    """
    API endpoint to update user.
    """
    permission_classes = (IsAuthenticated, IsAdminUser, ChangeUser)
    serializer_class = UpdateDetailUserSerializer
    queryset = User.objects.all()


class UserList(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ViewUser]
    
    class Pagination(LimitOffsetPagination):
        default_limit = 5
        max_limit = None

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = UserFilter(data=request.query_params)
        try:
            filters_serializer.is_valid()
        except ValidationError as exc:
            raise DRFValidationError(detail=exc.message_dict)

        users = user_list(filters=filters_serializer.data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=UserListSrializer,
            queryset=users,
            request=request,
            view=self,
        )


class UserDetails(RetrieveAPIView):
    
    """
    API endpoint to retrieve a User Details.
    """
    permission_classes = [IsAuthenticated, IsAdminUser, ViewUser]  
    queryset =User.objects.all()
    serializer_class = UpdateDetailUserSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

class UserDelete(DestroyAPIView):
    """
    API endpoint to delete a User instance.
    """
    permission_classes = [IsAuthenticated, IsAdminUser, DeleteUser]
    queryset = User.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message":"User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def perform_destroy(self, instance):
        instance.delete()

        
        






