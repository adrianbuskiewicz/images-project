from rest_framework import serializers
from .models import ImageFile
from serializer_permissions import serializers as permissions_serializers
from .permissions import BiggerSizePermission, OriginalImagePermission, LinksCreatingPermission


class ImageSerializer(serializers.ModelSerializer):
    big_thumbnail = permissions_serializers.ImageField(
        permission_classes=(BiggerSizePermission,),
        hide=True,
        read_only=True,
    )
    original_image = permissions_serializers.ImageField(permission_classes=(OriginalImagePermission,), hide=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ImageFile
        fields = (
            'user',
            'title',
            'date_uploaded',
            'small_thumbnail',
            'big_thumbnail',
            'original_image',
        )
        read_only_fields = (
            'user',
            'date_uploaded',
            'small_thumbnail',
        )


