from django.core.validators import FileExtensionValidator

validate_image_extension = FileExtensionValidator(
    allowed_extensions=['jpg', 'jpeg', 'png'],
)
