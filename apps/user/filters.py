import django_filters


# Models
from apps.user.models import User


# User List filter class
class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains', required=False)
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    is_moderator = django_filters.BooleanFilter(field_name='is_moderator')
    is_staff = django_filters.BooleanFilter(field_name='is_staff')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ('email', 'full_name', 'contact_number' ,'is_moderator', 'is_staff', 'is_active')

    




