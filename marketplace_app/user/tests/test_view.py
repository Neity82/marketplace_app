from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from order.models import Order, DeliveryType
from product.models import Category, Product
from user.models import CustomUser, UserProductView, Compare, CompareEntity

TEST_EMAIL = 'normal@user.com'
TEST_PASS = 'test1793'


class BaseViewTests(TestCase):
    """Базовые данные для тестирования"""

    @classmethod
    def setUpTestData(cls):
        avatar = SimpleUploadedFile(
            "avatar.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        cls.user = CustomUser.objects.create_user(
            email=TEST_EMAIL,
            password=TEST_PASS,
            phone=9991112233,
            avatar=avatar,
            last_name='Last',
            first_name='First',
            middle_name='Middle'
        )

        icon = SimpleUploadedFile(
            "icon.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        category = Category.objects.create(
            title='category',
            icon=icon
        )
        cls.count = 5

        for i in range(1, cls.count + 1):
            Product.objects.create(
                title=f'Product_{i}',
                category=category
            )
        for i in range(1, cls.count + 1):
            UserProductView.objects.create(
                user_id=cls.user,
                product_id=Product.objects.get(pk=i),
                datetime=timezone.now()
            )
        delivery = DeliveryType.objects.create(name='delivery')
        for i in range(1, 4):
            Order.objects.create(
                user_id=cls.user,
                delivery_id=delivery,
                payment='card',
                city=f'City_{i}',
                address=f'Address_{i}'
            )

        compare = Compare.objects.create(user_id=cls.user)
        for i in range(4):
            CompareEntity.objects.create(
                compare=compare,
                product=Product.objects.get(id=i+1)
            )


class UserAccountViewTests(BaseViewTests):
    """Тесты представления UserAccount"""

    def test_url_exists_at_desired_location(self):
        # Не авторизован
        response = self.client.get(f'/user/{self.user.id}/account/')
        self.assertEqual(response.status_code, 302)
        # Авторизован
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))
        response = self.client.get(f'/user/{self.user.id}/account/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))

        response = self.client.get(f'/user/{self.user.id}/account/')
        self.assertTemplateUsed(response, 'user/account.html')
        self.assertTrue('page_active' in response.context)
        self.assertEqual(response.context['page_active'], 'account_active')
        self.assertTrue('last_order' in response.context)
        self.assertTrue('product_view' in response.context)


class UserProfileViewTests(BaseViewTests):
    """Тесты представления UserProfile"""

    def test_url_exists_at_desired_location(self):
        # Не авторизован
        response = self.client.get(f'/user/{self.user.id}/profile/')
        self.assertEqual(response.status_code, 302)
        # Авторизован
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))
        response = self.client.get(f'/user/{self.user.id}/profile/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))

        response = self.client.get(f'/user/{self.user.id}/profile/')
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertTrue('page_active' in response.context)
        self.assertEqual(response.context['page_active'], 'profile_active')
        self.assertEqual(
            response.context['form'].initial['full_name'],
            'Last First Middle'
        )

    def test_correct_profile(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))
        url = f'/user/{self.user.id}/profile/'
        data_correct = {
            'email': 'new_email@test.ru',
            'phone': '+7(999) 111-22-44',
            'full_name': 'Old_last Old_first Old_middle',
        }
        response = self.client.post(url, data_correct)
        self.assertEqual(CustomUser.objects.get(id=1).email, 'new_email@test.ru')
        self.assertEqual(CustomUser.objects.get(id=1).phone, '9991112244')
        self.assertEqual(CustomUser.objects.get(id=1).last_name, 'Old_last')
        self.assertEqual(CustomUser.objects.get(id=1).first_name, 'Old_first')
        self.assertEqual(CustomUser.objects.get(id=1).middle_name, 'Old_middle')

        self.assertRedirects(response, f'/user/{self.user.id}/profile/', status_code=302,
                             target_status_code=200)


class HistoryOrderTests(BaseViewTests):
    """Тесты представления HistoryOrder"""

    def test_url_exists_at_desired_location(self):
        # Не авторизован
        response = self.client.get(f'/user/{self.user.id}/orders/')
        self.assertEqual(response.status_code, 302)
        # Авторизован
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))
        response = self.client.get(f'/user/{self.user.id}/orders/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))

        response = self.client.get(f'/user/{self.user.id}/orders/')
        self.assertTemplateUsed(response, 'user/historyorder.html')
        self.assertTrue('page_active' in response.context)
        self.assertEqual(response.context['page_active'], 'historyorder_active')

        self.assertQuerysetEqual(
            response.context['orders_list'],
            ['<Order: Order №3>',
             '<Order: Order №2>',
             '<Order: Order №1>']
        )


class HistoryViewTests(BaseViewTests):
    """Тесты представления HistoryView"""

    def test_url_exists_at_desired_location(self):
        # Не авторизован
        response = self.client.get(f'/user/{self.user.id}/views/')
        self.assertEqual(response.status_code, 302)
        # Авторизован
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))
        response = self.client.get(f'/user/{self.user.id}/views/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))

        response = self.client.get(f'/user/{self.user.id}/views/')
        self.assertTemplateUsed(response, 'user/historyview.html')
        self.assertTrue('page_active' in response.context)
        self.assertEqual(response.context['page_active'], 'historyview_active')

        self.assertEqual(len(response.context['views_list']), 5)


class CompareProductTests(BaseViewTests):
    """Тесты представления CompareProduct"""

    def test_url_exists_at_desired_location(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))

        response = self.client.get(f'/compare/category/0/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        self.assertTrue(self.client.login(email=TEST_EMAIL, password=TEST_PASS))

        response = self.client.get(f'/compare/category/0/')
        self.assertTemplateUsed(response, 'user/compare.html')
        self.assertTrue('categories' in response.context)
        self.assertTrue('cat_selected' in response.context)
        self.assertTrue('total_count' in response.context)
        self.assertTrue('attributes' in response.context)


class LoginTests(BaseViewTests):
    """Тесты представления CustomLoginView"""

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'user/login.html')

    def test_login(self):
        self.assertTrue(self.client.login(username=TEST_EMAIL, password=TEST_PASS))
        self.assertFalse(self.client.login(username='Test', password='password'))
        self.assertTrue(self.user.is_authenticated)


class SignUpTests(BaseViewTests):
    """Тесты представления SignUpView"""

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_sign_up(self):
        data = {
            'email': 'test@user.com',
            'password1': 'test1379',
            'password2': 'test1379',
        }
        self.assertEqual(CustomUser.objects.count(), 1)
        self.client.post(reverse('user:signup'), data)
        self.assertEqual(CustomUser.objects.count(), 2)

