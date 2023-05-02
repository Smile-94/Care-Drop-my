from django.db.models import ProtectedError
from django.core.exceptions import ValidationError
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# Generic View Classes
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView

# Permission Classes
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import CreateBlog
from apps.common.permissions import UpdateBlogIsOwnerOrAdmin
from apps.common.permissions import DeleteBlogIsOwnerOrAdmin

# Models
from apps.blog.models import BlogPost

# Serializers Classes
from apps.blog.serializers import CreateUpdateBlogSerializer


class CreateBlogAPIView(CreateAPIView):
    serializer_class = CreateUpdateBlogSerializer
    permission_classes = [IsAuthenticated, CreateBlog]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.user.is_staff or request.user.is_moderator:
            message = 'Blog post created successfully.'
        else:
            message = 'Your post is now under review. We will get back to you soon'
        return Response({
            'message': message,
            'data': response.data
        }, status=response.status_code)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        if self.request.user.is_staff or self.request.user.is_moderator:
            serializer.save(status='published')
