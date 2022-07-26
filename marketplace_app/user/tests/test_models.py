import datetime

from django.test import TestCase
from django.utils import timezone

from product.models import Product, Category
from user.models import CustomUser, UserProductView, Compare, CompareEntity

from user.utils import avatar_directory_path


class CustomUserModelTests(TestCase):
    """Тесты для модели CustomUser"""

    def test_create_user(self):
        """Тест на добавление пользователя"""

        user = CustomUser.objects.create_user(
            email="normal@user.com", password="1234pass"
        )
        self.assertEqual(user.email, "normal@user.com")
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
            CustomUser.objects.create_user(email="")
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email="", password="1234pass")

    def test_create_superuser(self):
        """Тест на добавление суперпользователя"""

        admin_user = CustomUser.objects.create_superuser(
            email="super@user.com", password="1234pass"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email="super@user.com", password="1234pass", is_superuser=False
            )

    def test_avatar_directory_path(self):
        """
        Тест функции avatar_directory_path,
        создание пути для сохранения аватарки
        """

        user = CustomUser.objects.create_user(
            email="test@test.com", password="1234pass"
        )
        self.assertTrue(CustomUser.objects.get(email="test@test.com"))

        result = avatar_directory_path(user, "testavatar.jpg")
        self.assertEqual(result, "avatar/user_1/('testavatar', '.jpg')")

    def test_verbose_name(self):
        user = CustomUser.objects.create_user(
            email="test@test.com", password="1234pass"
        )
        self.assertEqual(user._meta.get_field("email").verbose_name, "email")
        self.assertEqual(user._meta.get_field("first_name").verbose_name, "first name")
        self.assertEqual(
            user._meta.get_field("middle_name").verbose_name, "middle name"
        )
        self.assertEqual(user._meta.get_field("last_name").verbose_name, "last name")
        self.assertEqual(user._meta.get_field("phone").verbose_name, "phone")
        self.assertEqual(user._meta.get_field("avatar").verbose_name, "avatar")

    def test_str(self):
        """Тест строкового представления объекта"""

        user = CustomUser.objects.create_user(
            email="test@test.com",
            password="1234pass",
            first_name="First",
            middle_name="Middle",
            last_name="Last",
        )
        self.assertEqual(str(user), "Last F.M.")

    def test_get_full_name(self):
        """Тест функции get_full_name, получение полного ФИО пользователя"""

        user1 = CustomUser.objects.create_user(
            email="test1@test.com", password="1234pass"
        )
        self.assertEqual(user1.get_full_name, "")
        user2 = CustomUser.objects.create_user(
            email="test2@test.com",
            password="1234pass",
            first_name="First",
            last_name="Last",
        )
        self.assertEqual(user2.get_full_name, "Last First")
        user3 = CustomUser.objects.create_user(
            email="test3@test.com",
            password="1234pass",
            first_name="First",
            middle_name="Middle",
            last_name="Last",
        )
        self.assertEqual(user3.get_full_name, "Last First Middle")


class BaseModelTests(TestCase):
    """Базовые данные для тестирования"""

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test1@test.com",
            password="1234pass",
            first_name="First_name",
            last_name="Last_name",
        )
        category = Category.objects.create(title="category_1")
        cls.count_item = 5
        for i in range(1, cls.count_item + 1):
            Product.objects.create(
                title=f"product_{i}",
                category=category,
            )


class UserProductViewModelTests(BaseModelTests):
    """Тест модели UserProductView"""

    def test_create_user_product_view(self):
        """Тест на добавление нового объекта модели"""

        UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first(),
            datetime=timezone.now(),
        )
        self.assertEqual(UserProductView.objects.count(), 1)

    def test_verbose_name(self):
        product_view = UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first(),
            datetime=timezone.now(),
        )
        self.assertEqual(product_view._meta.get_field("user_id").verbose_name, "user")
        self.assertEqual(
            product_view._meta.get_field("product_id").verbose_name, "product"
        )
        self.assertEqual(
            product_view._meta.get_field("datetime").verbose_name,
            "datetime of addition",
        )

    def test_str(self):
        """Тест строкового представления объекта"""

        product_view = UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first(),
            datetime=timezone.now(),
        )
        self.assertEqual(str(product_view), str(product_view.product_id))

    def test_get_product_view(self):
        """
        Тест функции get_product_view,
        получение списка просмотренных товаров
        """

        for item in Product.objects.all():
            UserProductView.objects.create(
                user_id=self.user, product_id=item, datetime=timezone.now()
            )
        count = UserProductView.objects.count()
        self.assertEqual(count, self.count_item)

        # Не задан параметр limit, получаем весь список
        self.assertEqual(
            len(UserProductView.get_product_view(user=self.user)), self.count_item
        )
        # Параметр limit = 2, получаем список из двух объектов
        self.assertEqual(
            len(UserProductView.get_product_view(user=self.user, limit=2)), 2
        )
        # Параметр limit = 10 (больше чем существует объектов в модели,
        # получаем список из всех имеющихся объектов модели
        self.assertEqual(
            len(UserProductView.get_product_view(user=self.user, limit=10)),
            self.count_item,
        )

    def test_add_object(self):
        """
        Тест функции add_object,
        добавление товара в просмотренные
        """

        product_view_old = UserProductView.objects.create(
            user_id=self.user,
            product_id=Product.objects.first(),
            datetime=timezone.now() - datetime.timedelta(days=1),
        )
        count = UserProductView.objects.count()
        self.assertEqual(count, count)
        # Если нет товара среди просмотренных - добавляем
        UserProductView.add_object(user=self.user, product=Product.objects.all()[1])
        count = UserProductView.objects.count()
        self.assertEqual(count, count)

        datetime_1 = UserProductView.objects.get(
            user_id=self.user, product_id=Product.objects.first()
        ).datetime
        # Товар есть в списке просмотренных - обновляем дату просмотра
        UserProductView.add_object(user=self.user, product=product_view_old.product_id)
        product_view_new = UserProductView.objects.get(
            user_id=self.user, product_id=Product.objects.first()
        )
        datetime_2 = product_view_new.datetime

        self.assertNotEqual(datetime_1, datetime_2)


class CompareEntityModelTest(BaseModelTests):
    def test_create_compare_entity(self):
        """Тест на добавление нового объекта модели"""
        compare = Compare.objects.create(user_id=self.user)
        compare_entity = CompareEntity.objects.create(
            product=Product.objects.first(), compare=compare
        )
        self.assertEqual(CompareEntity.objects.count(), 1)

        self.assertEqual(
            compare_entity._meta.get_field("product").verbose_name, "product"
        )
        self.assertEqual(
            compare_entity._meta.get_field("compare").verbose_name, "compare's"
        )

    def test_str(self):
        """Тест строкового представления объекта"""

        compare = Compare.objects.create(user_id=self.user)
        compare_entity = CompareEntity.objects.create(
            product=Product.objects.first(), compare=compare
        )
        self.assertEqual(
            str(compare_entity),
            f"Compare entity: user {self.user}, product: {Product.objects.first()}",
        )


class CompareModelTests(BaseModelTests):
    """Тесты модели Compare"""

    def test_create_compare(self):
        """Тест на добавление нового объекта модели"""

        Compare.objects.create(user_id=self.user)
        self.assertEqual(Compare.objects.count(), 1)

    def test_verbose_name(self):
        compare = Compare.objects.create(user_id=self.user)
        self.assertEqual(compare._meta.get_field("user_id").verbose_name, "user")
        self.assertEqual(compare._meta.get_field("device").verbose_name, "device")

    def test_str(self):
        """Тест строкового представления объекта"""
        device = "aaa111sss222"
        compare = Compare.objects.create(user_id=self.user, device=device)
        self.assertEqual(str(compare), f"Compare: user: {self.user}, device: {device}")

    def test_get_compare_lis(self):
        """
        Тест функции get_compare_list,
        получение списка товаров для сравнения
        """

        compare = Compare.objects.create(user_id=self.user)
        for item in Product.objects.all():
            CompareEntity.objects.create(compare=compare, product=item)
        compare_list = Compare.get_compare_list(compare_id=compare.id)
        self.assertEqual(len(compare_list), self.count_item)

    def test_add_to_compare(self):
        """
        Тест функции add_to_compare,
        Добавляем товар в сравнение если его там нет
        """

        compare = Compare.objects.create(user_id=self.user)
        CompareEntity.objects.create(compare=compare, product=Product.objects.first())
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 1)

        # Пробуем добавить товар, который уже есть в сравнении
        res, mess = compare.add_to_compare(product_id=Product.objects.first().id)
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 1)
        self.assertEqual(res, False)
        self.assertEqual(mess, "has already been added before")

        # Пробуем добавить новый товар
        res, mess = compare.add_to_compare(product_id=Product.objects.all()[1].id)
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 2)
        self.assertEqual(res, True)
        self.assertEqual(mess, "successfully added")

        # Пробуем добавить товар сверх лимита
        CompareEntity.objects.create(compare=compare, product=Product.objects.all()[2])
        CompareEntity.objects.create(compare=compare, product=Product.objects.all()[3])
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 4)

        res, mess = compare.add_to_compare(product_id=Product.objects.all()[4].id)
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 4)
        self.assertEqual(res, False)
        self.assertEqual(mess, "maximum of products for comparison")

    def test_remove_from_compare(self):
        """
        Тест функции remove_from_compare
        Удаляем элемент сравнения
        """

        compare = Compare.objects.create(user_id=self.user)
        CompareEntity.objects.create(compare=compare, product=Product.objects.first())
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 1)

        res, mess = compare.remove_from_compare(product_id=Product.objects.first().id)
        self.assertEqual(CompareEntity.objects.filter(compare=compare).count(), 0)
        self.assertEqual(res, True)
        self.assertEqual(mess, "successfully removed")

    def test_count(self):
        """
        Тест функции count
        количество товаров для сравнения
        """

        compare = Compare.objects.create(user_id=self.user)
        CompareEntity.objects.create(compare=compare, product=Product.objects.first())

        count = Compare.count(compare_id=compare.id)
        self.assertEqual(count, 1)
