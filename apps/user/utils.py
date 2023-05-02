from django.core.exceptions import ValidationError
from PIL import Image


#function to custom user photo directory
def user_directory_path(instance,filename):
    return '{0}/{1}'.format(instance.full_name,filename)

# function to custom profile image validator
def validate_image_dimention(image):
    with Image.open(image) as img:
        width, height = img.size
        if width > 400 or height > 400:
            raise ValueError("Image height and width should be 300px or less")
        

# function to custom image file type validator
def validate_image_type(value):
    try:
        img = Image.open(value)
        # Check if the image is of type JPEG, PNG, or GIF
        if img.format not in ('JPEG','jpg', 'PNG',):
            raise ValidationError("Image must be of type JPEG, PNG, or GIF")

    except:
        raise ValidationError("Invalid image type")