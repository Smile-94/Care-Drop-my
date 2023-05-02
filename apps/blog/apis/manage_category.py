from django.db.models import ProtectedError
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# Permission Classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from apps.common.permissions import AddCategory
from apps.common.permissions import UpdateCategory
from apps.common.permissions import DeleteCategory



# Import Models
from apps.blog.models import BlogCategory

# Serializers Classes
from apps.blog.serializers import CategorySerializer


# Add, Update, View, Blog Category
class CategoryView(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = CategorySerializer
    
    # Apply AdminOnlyPermission to create, update, and delete actions
    permission_classes_by_action = {
        'create': [IsAuthenticated, IsAdminUser, AddCategory],
        'update': [IsAuthenticated, IsAdminUser, UpdateCategory],
        'delete': [IsAuthenticated, IsAdminUser, DeleteCategory],
    }

    # serializer_classes = {
    #     'retrieve' : AuthorBlogDetailSerializer,
    #     'update': CreateUpdateBlogSerializers,
    #     'create' : CreateUpdateBlogSerializers
    # }

    def get_permissions(self):
        # Get the permission_classes for the current action
        permission_classes = self.permission_classes_by_action.get(
            self.action, [permissions.AllowAny]
        )
        return [permission() for permission in permission_classes]
    

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        message = {'message': 'Category has been created successfully'}
        response.data.update(message)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        message = {'message': 'Category has been updated successfully'}
        response.data.update(message)
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = {'message': 'Category has been deleted successfully'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
            try:
                instance.delete()
            except ProtectedError:
                raise ValidationError("This category is associated with some blog posts and cannot be deleted.")
            except ValidationError as e:
                raise ValidationError(e.message)