from rest_framework import generics, views, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions
from .models import ImageFile
from .serializers import ImageSerializer, ExpiringLinkCreateSerializer
from .permissions import LinksCreatingPermission
from .models import ExpiringLink
from django.utils import timezone
import datetime
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from secrets import token_urlsafe

# Create your views here.


class ImageUploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.user = request.user
            serializer.save()
            return Response('Image uploaded!', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(generics.RetrieveAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = ImageSerializer


class ImageListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user.id
        qs = ImageFile.objects.filter(user=user)
        if qs:
            return qs
        else:
            return None


class ExpiringLinkCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, LinksCreatingPermission]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ExpiringLinkCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data
            img = get_object_or_404(ImageFile, id=data['img_id'])
            token = token_urlsafe(20)
            url = request.build_absolute_uri(f'/api/{token}')
            link = ExpiringLink(
                image=img,
                token=token,
                expiring_url=url,
                time_to_expire=timezone.now()+datetime.timedelta(seconds=data['seconds']),
            )
            link.save()
            return Response(url, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def expiring_image_view(request, token):
    try:
        token = ExpiringLink.objects.get(token=token, time_to_expire__gte=timezone.now())
        image = get_object_or_404(ImageFile, id=token.image.id).original_image
        extension = str(image).split('.')[1]
        extension = 'jpeg' if extension in ('jpg', 'jpeg') else 'png'
        return HttpResponse(image, content_type=f"image/{extension}")
    except ExpiringLink.DoesNotExist:
        return Response('Link\'s time expired!', status=status.HTTP_400_BAD_REQUEST)