from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .views import image_upload_view


class ImageUploadViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_image_upload_view(self):
        # Assuming your URL pattern for `image_upload_view` is named 'image-upload'
        url = reverse('upload-image')

        # Open the image file you want to upload
        with open('/home/nishad/Downloads/product-1.jpg', 'rb') as image_file:
            # Create a dictionary containing the file data
            data = {'image': image_file}

            # Send a POST request to the API endpoint
            response = self.client.post(url, data, format='multipart')

            # Assert that the response status code is 201 (Success)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Optionally, you can assert the response content or other data as needed
            # self.assertEqual(response.data['message'], 'Image is received!!!')
            # self.assertEqual(
            #     response.data['image_url'], '/home/nishad/Downloads/product-1.jpg')
