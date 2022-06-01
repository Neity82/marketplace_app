from django.test import TestCase

from .models import Shop


class ShopTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shop = Shop.objects.create(name="test shop 1", image='computers_shop.jpg')

    def test_shop_instance_creation(self):
        shop = Shop.objects.get(name="test shop 1")
        self.assertEqual(shop.name, 'test shop 1')

    def test_shop_list_endpoint(self):
        response = self.client.get('/shops/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_list.html')

    def test_shop_detail_endpoint(self):
        response = self.client.get('/shops/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_detail.html')
