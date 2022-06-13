from rest_framework import serializers
from .models import ImageFile, ExpiringLink
from serializer_permissions import serializers as permissions_serializers
from .permissions import BiggerSizePermission, OriginalImagePermission, LinksCreatingPermission


class LinkSerializer(serializers.ModelSerializer):
    expire_time = serializers.DateTimeField(source='time_to_expire')
    expiring_url = permissions_serializers.URLField(permission_classes=(LinksCreatingPermission,))

    class Meta:
        model = ExpiringLink
        fields = (
            'expire_time',
            'expiring_url',
        )


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    big_thumbnail = permissions_serializers.ImageField(
        permission_classes=(BiggerSizePermission,),
        hide=True,
        read_only=True,
    )
    original_image = permissions_serializers.ImageField(permission_classes=(OriginalImagePermission,), hide=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expiring_links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = ImageFile
        fields = (
            'id',
            'user',
            'title',
            'date_uploaded',
            'small_thumbnail',
            'big_thumbnail',
            'original_image',
            'expiring_links',
        )
        read_only_fields = (
            'id',
            'user',
            'date_uploaded',
            'small_thumbnail',
        )


class ExpiringLinkCreateSerializer(serializers.Serializer):
    img_id = serializers.CharField()
    seconds = serializers.IntegerField(default=300, min_value=300, max_value=30000)

    class Meta:
        fields = (
            'img_id',
            'seconds',
        )
