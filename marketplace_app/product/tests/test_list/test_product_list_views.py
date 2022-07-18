import itertools
import os
from random import randint, sample, choice
# import pytest
import typing

from django.test import TestCase
from django.db.models import Q
from urllib import parse

from product import models as product_models

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FIXTURES_DIR = os.path.join(CURRENT_DIR, "fixtures")

FIXTURES = [
    os.path.join(FIXTURES_DIR, "product.json"),
    os.path.join(FIXTURES_DIR, "discount.json"),
    os.path.join(FIXTURES_DIR, "shop.json"),
    os.path.join(FIXTURES_DIR, "atribute.json"),
]


class ProductListTest(TestCase):
    base_url = "/catalog/"
    template_name = "product/catalog.html"
    fixtures = FIXTURES

    @staticmethod
    def _get_random_product() -> product_models.Product:
        return product_models.Product.objects.all()\
                                             .order_by('?')\
                                             .first()

    @staticmethod
    def _get_random_category() -> product_models.Category:
        return product_models.Category.objects.all()\
                                          .order_by('?')\
                                          .first()

    # @pytest.mark.django_db
    def _test_post_request(self, data: dict) -> parse.SplitResult:
        response = self.client.post(self.base_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(hasattr(response, 'url'))
        return parse.urlsplit(response.url)

    # @pytest.mark.django_db
    def _test_price_filter(self, data: dict,
                           price_first: int, price_second: int) -> None:
        price_range = '%d;%d' % (price_first, price_second)
        url = self._test_post_request(data=data)
        qs_params = parse.parse_qs(url.query)
        self.assertIn('price', qs_params)
        self.assertIn(price_range, qs_params.get('price', ''))
        response = self.client.get(url.path, data=qs_params)
        self.assertEqual(response.status_code, 200)
        products: list = response.context_data.get('products', [])
        for product in products:
            self.assertGreaterEqual(product.discount['price'], price_first)
            self.assertLessEqual(product.discount['price'], price_second)

    # @pytest.mark.django_db
    def _test_shop_filter(self, data: dict, shops_filter: list) -> None:
        url = self._test_post_request(data=data)
        qs_params = parse.parse_qs(url.query)
        self.assertIn('shop', qs_params)
        for shop_id in shops_filter:
            self.assertIn(str(shop_id), qs_params['shop'])
        response = self.client.get(url.path, data=qs_params)
        self.assertEqual(response.status_code, 200)
        products: list = response.context_data.get('products', [])
        for product in products:
            product_shops = [
                item[0]
                for item
                in product_models.Stock.objects.only('shop__id')
                                               .filter(product=product)
                                               .values_list('shop__id')]
            self.assertTrue(
                any([
                    (product_shop in shops_filter)
                    for product_shop
                    in product_shops
                ])
            )

    # @pytest.mark.django_db
    def _test_title_filter(self, data: dict, search_text: str) -> None:
        url = self._test_post_request(data=data)
        qs_params = parse.parse_qs(url.query)
        self.assertIn('title', qs_params)
        self.assertIn(search_text, qs_params.get('title', ''))
        response = self.client.get(url.path, data=qs_params)
        self.assertEqual(response.status_code, 200)
        products: list = response.context_data.get('products', [])
        for product in products:
            self.assertIn(search_text.lower(), product.title.lower())

    # @pytest.mark.django_db
    def test_get(self) -> None:
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    # @pytest.mark.django_db
    def test_sorting(self, ext_data=dict()) -> None:

        sortings: typing.List[dict] = [
            {'sorting': '', 'property_name': 'discount',
                            'dict_key': 'price'},
            {'sorting': 'invalid', 'property_name': 'discount',
                                   'dict_key': 'price'},
            {'sorting': 'price', 'property_name': 'discount',
                                 'dict_key': 'price'},
            {'sorting': '-price', 'property_name': 'discount',
                                  'dict_key': 'price'},
            {'sorting': 'popularity', 'property_name': 'popularity',
                                      'dict_key': None},
            {'sorting': '-popularity', 'property_name': 'popularity',
                                       'dict_key': None},
            {'sorting': 'review', 'property_name': 'reviews',
                                  'dict_key': None},
            {'sorting': '-review', 'property_name': 'reviews',
                                   'dict_key': None},
            {'sorting': 'novelty', 'property_name': 'created_at',
                                   'dict_key': None},
            {'sorting': '-novelty', 'property_name': 'created_at',
                                    'dict_key': None},
        ]

        for item in sortings:
            sorting = item['sorting']
            property_name = item['property_name']
            dict_key = item['dict_key']
            reverse = sorting.startswith('-')
            data = ext_data.copy()
            if sorting:
                data.update(
                    {'sort_by': sorting}
                )
            response = self.client.get(self.base_url, data=data)
            self.assertEqual(response.status_code, 200)
            products: list = response.context_data.get('products', [])
            if not products:
                return
            self.assertTrue(
                all([
                    hasattr(product, property_name)
                    for product
                    in products
                ])
            )
            property_is_dict = all([
                    isinstance(getattr(product, property_name), dict)
                    for product
                    in products
                ])
            if not property_is_dict:
                self.assertFalse(
                    any([
                            isinstance(getattr(product, property_name), dict)
                            for product
                            in products
                        ])
                )
            for idx in range(1, len(products)):
                item_a = (
                    (getattr(products[idx-1], property_name)).get(dict_key)
                    if property_is_dict
                    else getattr(products[idx-1], property_name)
                )
                item_b = (
                    (getattr(products[idx], property_name)).get(dict_key)
                    if property_is_dict
                    else getattr(products[idx], property_name)
                )
                if reverse:
                    self.assertGreaterEqual(item_a, item_b)
                else:
                    self.assertLessEqual(item_a, item_b)

    # @pytest.mark.django_db
    def test_base_filters(self, ext_data=dict()) -> None:
        # получаем базовый набор параметров, идентичный для всех фильтров
        response = self.client.get(self.base_url, data=ext_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('min_price', response.context_data)
        self.assertIn('max_price', response.context_data)
        min_price = response.context_data['min_price']
        max_price = response.context_data['max_price']
        self.assertIn('shops', response.context_data)
        shops = response.context_data['shops']
        filters = ['price', 'title', 'shops']
        for items_count in range(1, len(filters)):
            for variant in itertools.combinations(filters, items_count):
                # сбрасываем параметры запроса
                data: dict = ext_data.copy()
                data.update({'price': '%d;%d' % (min_price, max_price)})
                # параметры для фильтра price
                if 'price' in variant:
                    if (max_price - min_price) > 5:
                        middle_price = round((min_price + max_price) / 2)
                        price_first = randint(min_price, middle_price)
                        price_second = randint(price_first + 1, max_price)
                    else:
                        price_first = min_price
                        price_second = max_price
                    price_range = '%d;%d' % (price_first, price_second)
                    data.update({'price': price_range})
                # параметры фильтра shop
                if 'shops' in variant:
                    shops_filter = sample(
                        [shop.id for shop in shops], k=randint(1, len(shops))
                    )
                    data.update({'shop': shops_filter})
                # параметры фильтра title
                if 'title' in variant:
                    product = self._get_random_product()
                    search_text: str = product.title.split(' ')[0]
                    data.update({'title': search_text})
                if 'price' in variant:
                    self._test_price_filter(data, price_first, price_second)
                if 'shops' in variant:
                    self._test_shop_filter(data, shops_filter)
                if 'title' in variant:
                    self._test_title_filter(data, search_text)
                self.test_sorting(ext_data=data)

    # @pytest.mark.django_db
    def test_header_search(self) -> None:
        product = self._get_random_product()
        search_text: str = product.title.split(' ')[0]
        data = {'query': search_text}
        url = self._test_post_request(data=data)
        qs_params = parse.parse_qs(url.query)
        self.assertEqual(len(qs_params), 1)
        self.assertIn('query', qs_params)
        self.assertIn(search_text, qs_params.get('query', ''))
        response = self.client.get(url.path, data=qs_params)
        self.assertEqual(response.status_code, 200)
        products: list = response.context_data.get('products', [])
        for product in products:
            self.assertIn(search_text.lower(), product.title.lower())
        self.test_sorting(ext_data=data)

    # @pytest.mark.django_db
    def test_category_link(self) -> None:
        category = self._get_random_category()
        data = {'category': category.id}
        response = self.client.get(self.base_url, data=data)
        self.assertEqual(response.status_code, 200)
        products: list = response.context_data.get('products', [])
        for product in products:
            self.assertEqual(product.category, category)
        self.test_sorting(ext_data=data)

    # @pytest.mark.django_db
    def test_attribute_filters(self) -> None:
        category = self._get_random_category()
        data = {'category': category.id}
        response = self.client.get(self.base_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('attributes', response.context_data)
        for attribute in response.context_data['attributes']:
            temp_data = data.copy()
            if attribute['type'] == 'C':
                selected_value = 'on'
                temp_data.update(
                    {'attr_c_%d' % attribute['id']: selected_value}
                )
            elif attribute['type'] == 'S':
                selected_value = choice(list(attribute['values']))
                temp_data.update(
                    {'attr_s_%d' % attribute['id']: selected_value}
                )
            elif attribute['type'] == 'T':
                selected_value = \
                    choice(list(attribute['values'])).split(sep=' ')[0]
                temp_data.update(
                    {'attr_t_%d' % attribute['id']: selected_value}
                )
            response = self.client.get(self.base_url, temp_data)
            products: list = response.context_data.get('products', [])
            for product in products:
                attr_value = \
                    product_models.AttributeValue.objects.filter(
                        Q(product=product) &
                        Q(attribute__id=attribute['id'])
                    )
                self.assertEqual(len(attr_value), 1)
                value = attr_value.first().value
                if attribute['type'] == 'C':
                    self.assertEqual(value.lower(), 'yes')
                elif attribute['type'] == 'S':
                    self.assertEqual(value, selected_value)
                elif attribute['type'] == 'T':
                    self.assertIn(selected_value.lower(), value.lower())
            self.test_sorting(ext_data=data)
