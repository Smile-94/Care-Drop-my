
# Generics Views
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView

# Permission Classes
from rest_framework.permissions import IsAuthenticated

# Custom Permission Classes
from apps.user.permissions import OwnProfilePermission

# Models
from apps.user.models import User

# Serializers
from apps.user.serializers import ProfileSerializer


class Profile(RetrieveAPIView):
    permission_classes = (IsAuthenticated, OwnProfilePermission)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

class ProfileUpdate(UpdateAPIView):
    """
    API endpoint for updating a user's profile.
    """
    permission_classes = (IsAuthenticated, OwnProfilePermission)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

