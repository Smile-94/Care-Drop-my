from rest_framework import serializers

# Tag it Serializers
from taggit.serializers import TagListSerializerField
from taggit.serializers import TaggitSerializer

# Models 
from apps.blog.models import BlogCategory
from apps.blog.models import BlogPost

class CategorySerializer(serializers.ModelSerializer):
        
    class Meta:
        model = BlogCategory
        fields = ( 'id','name', 'created_at', 'updated_at')
        read_only_fields = ( 'id', 'created_at', 'updated_at')
        extra_kwargs = {
            'created_at': {'required': False},
            'updated_at': {'required': False}
        }

class CategoryPresentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = ('id','name')


class CreateUpdateBlogSerializer( TaggitSerializer,serializers.ModelSerializer):

    
    keywords  = TagListSerializerField()

    class Meta:
        model = BlogPost
        fields = ('title','content', 'category','post_image','keywords')
        extra_kwargs = {
            'post_image': {'required': False},
            'keywords': {'required': False}
        }
    
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user

        # Set the published status to "published" if the user is staff or moderator
        if self.context['request'].user.is_staff or self.context['request'].user.is_moderator:
            validated_data['status'] = 'published'
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryPresentSerializer(instance.category.all(), many=True).data
        return data
    



class BlogDetailsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = BlogPost
        fields = ('author','title')


        