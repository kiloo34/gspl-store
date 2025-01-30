from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from catalog.models import Product
from django.utils.timezone import now

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

        self.product1 = Product.objects.create(name="Product 1", description="First product", price_idr=2000000.00)
        self.product2 = Product.objects.create(name="Product 2", description="Second product", price_idr=3000000.00)

        self.valid_product_data = {"name": "Test Product", "description": "This is a test product", "price_idr": 1000000.00}
        self.invalid_product_data = {"name": "", "description": "Invalid product", "price_idr": -1000000.00}

        self.products_url = "/api/products/"

    def test_create_product(self):
        invalid_data = {"name": "", "description": "Invalid product", "price_idr": -500000.00}
        response = self.client.post(self.products_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_fields = {"invalid_field": "test"}
        response = self.client.post(self.products_url, invalid_fields, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.products_url, self.valid_product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.valid_product_data["name"])

        self.client.logout()

        response = self.client.post(self.products_url, self.valid_product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product(self):
        product = Product.objects.create(name="Test Product", description="Initial product", price_idr=1000000.00)
        
        invalid_data = {"name": "", "description": "Updated product", "price_idr": -500000.00}
        response = self.client.put(f"{self.products_url}{product.id}/", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(f"{self.products_url}{product.id}/", {"invalid_field": "test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        valid_update = {"name": "Updated Product", "description": "Updated description", "price_idr": 1500000.00}
        response = self.client.put(f"{self.products_url}{product.id}/", valid_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], valid_update["name"])

        self.client.logout()
        
        valid_update = {"name": "Updated Product", "description": "Updated description", "price_idr": 1500000.00}
        response = self.client.put(f"{self.products_url}{product.id}/", valid_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_products(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_product_by_id(self):
        response = self.client.get(f"{self.products_url}{self.product1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product1.name)

    def test_get_soft_deleted_product_by_id(self):
        self.product1.soft_delete()
        response = self.client.get(f"{self.products_url}{self.product1.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_delete_product(self):
        response = self.client.delete(f"{self.products_url}{self.product1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product1.refresh_from_db()
        self.assertTrue(self.product1.is_deleted())

        response = self.client.get(f"{self.products_url}{self.product1.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_products_excludes_soft_deleted(self):
        self.product1.soft_delete()
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)