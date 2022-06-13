from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from PIL import Image
import tempfile
from rest_framework.authtoken.models import Token
from .models import CustomUser, Tier


class TestCreateImageFiles(APITestCase):

    def temp_image(self, height=100, width=100):
        image = Image.new('RGB', (height, width))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        return tmp_file

    def authenticate(self, big_size, org_link, exp_link):
        self.tier, self.created = Tier.objects.get_or_create(
            can_bigger_size=big_size,
            can_original_image=org_link,
            can_expiring_link=exp_link,
        )
        self.user = CustomUser(username='matthew', password='testing55', tier=self.tier)
        self.user.save()
        self.client = APIClient()

        self.token = Token.objects.get(user__username='matthew')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_image_file(self):
        self.authenticate(True, True, True)
        data = {
            'original_image': self.temp_image(),
            'title': 'hehe',
        }
        response = self.client.post(reverse('image_upload'), data=data, format='multipart')

        self.assertEqual(response.json(), 'Image uploaded!')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_image_list_can_not_bigger_size(self):
        self.authenticate(False, False, False)

        data = {
            'original_image': self.temp_image(100, 100),
            'title': 'image1',
        }
        data2 = {
            'original_image': self.temp_image(200, 200),
            'title': 'image2',
        }

        self.client.post(reverse('image_upload'), data=data, format='multipart')
        self.client.post(reverse('image_upload'), data=data2, format='multipart')
        response = self.client.get(reverse('image_list'))

        image1_title = 'image1'
        image2_big_thumbnail = None

        self.assertEqual(response.json()[0]['title'], image1_title)
        self.assertEqual(response.json()[1]['big_thumbnail'], image2_big_thumbnail)

    def test_get_image_list_can_bigger_size(self):
        self.authenticate(True, False, False)

        data = {
            'original_image': self.temp_image(100, 100),
            'title': 'image1',
        }
        data2 = {
            'original_image': self.temp_image(200, 200),
            'title': 'image2',
        }

        self.client.post(reverse('image_upload'), data=data, format='multipart')
        self.client.post(reverse('image_upload'), data=data2, format='multipart')
        response = self.client.get(reverse('image_list'))

        image1_title = 'image1'
        image2_big_thumbnail = 'jpg'

        response_big_thumbnail = response.json()[1]['big_thumbnail']

        self.assertEqual(response.json()[0]['title'], image1_title)
        self.assertEqual(response_big_thumbnail.split('.')[1], image2_big_thumbnail)

    def test_get_image_list_can_not_original_image(self):
        self.authenticate(True, False, False)

        data = {
            'original_image': self.temp_image(100, 100),
            'title': 'image1',
        }

        self.client.post(reverse('image_upload'), data=data, format='multipart')
        response = self.client.get(reverse('image_list'))

        image_title = 'image1'
        original_image = None

        response_original_image = response.json()[0]['original_image']

        self.assertEqual(response.json()[0]['title'], image_title)
        self.assertEqual(response_original_image, original_image)

    def test_get_image_list_can_original_image(self):
        self.authenticate(True, True, False)

        data = {
            'original_image': self.temp_image(100, 100),
            'title': 'image1',
        }

        self.client.post(reverse('image_upload'), data=data, format='multipart')
        response = self.client.get(reverse('image_list'))

        image_title = 'image1'
        original_image = 'jpg'

        response_original_image = response.json()[0]['original_image']

        self.assertEqual(response.json()[0]['title'], image_title)
        self.assertEqual(response_original_image.split('.')[1], original_image)

    def test_get_image_list_can_not_create_expiring_links(self):
        self.authenticate(True, True, False)

        data_image = {
            'original_image': self.temp_image(100, 100),
            'title': 'image1',
        }

        self.client.post(reverse('image_upload'), data=data_image, format='multipart')
        created_image = self.client.get(reverse('image_list'))

        data_link = {
            'img_id': created_image.json()[0]['id'],
            'seconds_300': 300,
        }
        response = self.client.post(reverse('image_expiring_link'), data=data_link, format='multipart')

        self.assertEqual(response.json()['detail'], 'Tier does not allow to create expiring links.')

    def test_get_image_list_can_create_expiring_links(self):
        self.authenticate(True, True, True)

        data_image = {
            'original_image': self.temp_image(100, 100),
            'title': 'image1',
        }

        self.client.post(reverse('image_upload'), data=data_image, format='multipart')
        created_image = self.client.get(reverse('image_list'))

        data_link = {
            'img_id': created_image.json()[0]['id'],
            'seconds_300': 300,
        }
        response = self.client.post(reverse('image_expiring_link'), data=data_link, format='multipart')

        self.assertEquals(response.json().startswith('http'), True)
