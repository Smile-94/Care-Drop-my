from rest_framework.permissions import BasePermission

class AddUser(BasePermission):
    """Allow access to create user only"""

    message = "Only  Staff has Permission to Add User!"

    def has_permission(self, request, view):
        return request.user.has_perm('users.add_user')


class ChangeUser(BasePermission):
    """Allow access to create user only"""

    message = "Only staff have permission to update user!"

    def has_permission(self, request, view):
        return request.user.has_perm('users.change_user')
      
class ViewUser(BasePermission):
    """Allow access to create user only"""

    message = "You don't have permission to view user!"

    def has_permission(self, request, view):
        return request.user.has_perm('users.view_user')


class DeleteUser(BasePermission):
    """Allow access to create user only"""

    message = "You don't have permission to view user!"

    def has_permission(self, request, view):
        return request.user.has_perm('users.delete_user')
    
# Category Permission
class AddCategory(BasePermission):
    """Allow access to create category only"""

    message = "Only Staff has Permission to Add Category!"

    def has_permission(self, request, view):
        return request.user.has_perm('users.add_category')
    
class UpdateCategory(BasePermission):
    """Allow access to update category only"""

    message = "Only Staff has Permission to Update Category!"

    def has_permission(self, request, view):
        return request.user.has_perm('users.update_category')
    

class DeleteCategory(BasePermission):
    """Allow access to View category only"""

    message = "Only Staff has Permission to Delete Category!"


# Blog Permission
class CreateBlog(BasePermission):
    """Allow access to create category only"""

    message = "Only registred user has Permission to Post Blog"

    def has_permission(self, request, view):
        return request.user.has_perm('users.add_category')


class UpdateBlogIsOwnerOrAdmin(BasePermission):
    """
    Custom permission class to only allow the owner or admin to update a blog post.
    """

    message = "Only staff and the blog owner have permission to update this blog post."

    def has_permission(self, request, view):
        # Allow all users to access the view
        return True

    def has_object_permission(self, request, view, obj):
        # Only allow staff and the blog owner to update the blog post
        if request.method in ['PUT', 'PATCH']:
            if request.user.is_staff or obj.author == request.user:
                return True
            else:
                self.message = "You are not authorized to update this blog post."
                return False
        # Allow all other methods to be accessed by all users
        return True
    

class DeleteBlogIsOwnerOrAdmin(BasePermission):
    """
    Custom permission class to only allow the owner or admin to delete a blog post.
    """

    message = "Only staff and the blog owner have permission to delete this blog post."

    def has_permission(self, request, view):
        # Allow all users to access the view
        return True

    def has_object_permission(self, request, view, obj):
        # Only allow staff and the blog owner to delete the blog post
        if request.method == 'DELETE':
            if request.user.is_staff or obj.author == request.user:
                return True
            else:
                self.message = "You are not authorized to delete this blog post."
                return False
        # Allow all other methods to be accessed by all users
        return True
