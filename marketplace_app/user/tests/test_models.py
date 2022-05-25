from django.test import TestCase

from product.models import Product, Category
from user.models import CustomUser, UserProductView, Compare

from user.utils import avatar_directory_path


class CustomUserModelTests(TestCase):
    """Тесты для модели CustomUser"""

    def test_create_user(self):
        """Тест на добавление пользователя"""

        user = CustomUser.objects.create_user(
            email='normal@user.com',
            password='1234pass'
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user()
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(email='')
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password="1234pass")

    def test_create_superuser(self):
        """Тест на добавление суперпользователя"""

        admin_user = CustomUser.objects.create_superuser(
            email='super@user.com',
            password='1234pass'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='super@user.com',
                password='1234pass',
                is_superuser=False
            )

    def test_avatar_directory_path(self):
        """
        Тест функции avatar_directory_path,
        создание пути для сохранения аватарки
        """

        user = CustomUser.objects.create_user(
            email='test@test.com',
            password='1234pass'
        )
        self.assertTrue(CustomUser.objects.get(email='test@test.com'))

        result = avatar_directory_path(user, 'testavatar.jpg')
        self.assertEqual(result, "avatar/user_1/('testavatar', '.jpg')")

    def test_verbose_name(self):
        user = CustomUser.objects.create_user(
            email='test@test.com',
            password='1234pass'
        )
        self.assertEqual(
            user._meta.get_field('email').verbose_name,
            'email'
        )
        self.assertEqual(
            user._meta.get_field('first_name').verbose_name,
            'first name'
        )
        self.assertEqual(
            user._meta.get_field('middle_name').verbose_name,
            'middle name'
        )
        self.assertEqual(
            user._meta.get_field('last_name').verbose_name,
            'last name'
        )
        self.assertEqual(
            user._meta.get_field('phone').verbose_name,
            'phone'
        )
        self.assertEqual(
            user._meta.get_field('avatar').verbose_name,
            'avatar'
        )

    def test_str(self):
        """Тест строкового представления объекта"""

        user = CustomUser.objects.create_user(
            email='test@test.com',
            password='1234pass',
            first_name='First',
            middle_name='Middle',
            last_name='Last'
        )
        self.assertEqual(str(user), 'Last F.M.')

    def test_get_full_name(self):
        """Тест функции get_full_name, получение полного ФИО пользователя"""

        user1 = CustomUser.objects.create_user(
            email='test1@test.com',
            password='1234pass'
        )
        self.assertEqual(user1.get_full_name, '')
        user2 = CustomUser.objects.create_user(
            email='test2@test.com',
            password='1234pass',
            first_name='First',
            last_name='Last'
        )
        self.assertEqual(user2.get_full_name, 'Last First')
        user3 = CustomUser.objects.create_user(
            email='test3@test.com',
            password='1234pass',
            first_name='First',
            middle_name='Middle',
            last_name='Last'
        )
        self.assertEqual(user3.get_full_name, 'Last First Middle')


class BaseModelTests(TestCase):
    """Базовые данные для тестирования"""

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email='test1@test.com',
            password='1234pass'
        )
        category = Category.objects.create(title='category_1')
        cls.count_item = 5
        for i in range(1, cls.count_item + 1):
            Product.objects.create(
                title=f'product_{i}',
                category=category,
            )


class UserProductViewModelTests(BaseModelTests):
    """Тест модели UserProductView"""

    def test_create_user_product_view(self):
        """Тест на добавление нового объекта модели"""

        UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first()
        )
        self.assertEqual(UserProductView.objects.count(), 1)

    def test_verbose_name(self):
        product_view = UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first()
        )
        self.assertEqual(
            product_view._meta.get_field('user_id').verbose_name,
            'user'
        )
        self.assertEqual(
            product_view._meta.get_field('product_id').verbose_name,
            'product'
        )
        self.assertEqual(
            product_view._meta.get_field('datetime').verbose_name,
            'datetime of addition'
        )

    def test_str(self):
        """Тест строкового представления объекта"""

        product_view = UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first()
        )
        self.assertEqual(str(product_view), str(product_view.product_id))

    def test_get_product_view(self):
        """
        Тест функции get_product_view,
        получение списка просмотренных товаров
        """

        for item in Product.objects.all():
            UserProductView.objects.create(
                user_id=self.user,
                product_id=item
            )
        count = UserProductView.objects.count()
        self.assertEqual(count, self.count_item)

        # Не задан параметр limit, получаем весь список
        self.assertEqual(
            len(UserProductView.get_product_view(user=self.user)),
            self.count_item
        )
        # Параметр limit = 2, получаем список из двух объектов
        self.assertEqual(
            len(UserProductView.get_product_view(user=self.user, limit=2)),
            2
        )
        # Параметр limit = 10 (больше чем существует объектов в модели,
        # получаем список из всех имеющихся объектов модели
        self.assertEqual(
            len(UserProductView.get_product_view(user=self.user, limit=10)),
            self.count_item
        )


class CompareModelTests(BaseModelTests):
    """Тесты модели Compare"""

    def test_create_compare(self):
        """Тест на добавление нового объекта модели"""

        Compare.objects.create(
            user_id=self.user,
            product_id=Product.objects.first()
        )
        self.assertEqual(Compare.objects.count(), 1)

    def test_verbose_name(self):
        compare = Compare.objects.create(
            user_id=self.user,
            product_id=Product.objects.first()
        )
        self.assertEqual(
            compare._meta.get_field('user_id').verbose_name,
            'user'
        )
        self.assertEqual(
            compare._meta.get_field('product_id').verbose_name,
            'product'
        )

    def test_str(self):
        """Тест строкового представления объекта"""

        compare = Compare.objects.create(
            user_id=self.user,
            product_id=Product.objects.first()
        )
        self.assertEqual(str(compare), str(compare.product_id))

    def test_get_compare_lis(self):
        """
        Тест функции get_compare_list,
        получение списка товаров для сравнения
        """

        for item in Product.objects.all():
            Compare.objects.create(
                user_id=self.user,
                product_id=item
            )
        compare_list = Compare.get_compare_list(user=self.user)
        self.assertEqual(len(compare_list), self.count_item)

    def test_get_count(self):
        """
        Тест функции get_count,
        получение количества товаров для сравнения
        """

        for item in Product.objects.all():
            Compare.objects.create(
                user_id=self.user,
                product_id=item
            )
        count = Compare.get_count(user=self.user)
        self.assertEqual(count, self.count_item)
