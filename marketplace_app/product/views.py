from urllib.parse import urlencode
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, TypedDict
from django.db.models import QuerySet, Sum, Count, Q, Avg, F
from django.db.models.functions import Coalesce

from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
from datetime import date, timedelta
from django.core.cache import cache

from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from info.models import Banner, Settings
from info.utils import DEFAULT_CACHE_TIME
from product.signals import get_product_detail_view
from shop.models import Shop
from product.forms import ProductReviewForm
from product import models


class IndexView(generic.TemplateView):
    """
        Представление страницы index.html

        - блок с баннерами;
        - три избранные категории товаров;
        - блок «Предложение дня»;
        - каталог топ-товаров;
        - слайдер с горячими предложениями;
        - слайдер с ограниченным тиражом
    """

    template_name = "product/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banner_list"] = Banner.get_banners()
        context["popular_category"] = models.Category.get_popular()
        context["popular_products"] = models.Product.get_popular()

        day = date.today() + timedelta(days=1)
        date_str = f"{day.day}.{day.month}.{day.year} 00:00"
        context["finish_day"] = date_str

        context["daily_offer"] = models.DailyOffer.get_daily_offer()
        context["hot_offers"] = models.Product.get_product_with_discount()
        context["limited_edition"] = models.Product.get_limited_edition(
            daily_offer=context["daily_offer"]
        )

        return context


class ProductListView(generic.ListView):
    """
        Представление страницы catalog.html

        - каталог товаров;
        - сортировка товаров;
    """
    template_name = "product/catalog.html"
    paginate_by = 8
    context_object_name = "products"

    def __init__(self, **kwargs: Any) -> None:
        self.query_params: Dict[str, Any] = {}
        super().__init__(**kwargs)

    def _get_sorted_list(self, queryset: QuerySet[models.Product],
                         sort_by: str) -> QuerySet[models.Product]:
        """Функция сортировки продуктов по одному из признаков

        :param queryset: Список продуктов
        :type queryset: QuerySet[Product]
        :param sort_by: Признак сортировки
        :type sort_by: str
        :return: Сортированный список продуктов
        :rtype: QuerySet[Product]
        """
        self.context["sort_by"] = sort_by
        if sort_by == "price":
            return sorted(
                queryset,
                key=lambda item: item.discount["price"]
            )
        elif sort_by == "-price":
            return sorted(
                queryset,
                key=lambda item: item.discount["price"],
                reverse=True
            )
        elif sort_by == "popularity":
            return sorted(
                queryset.annotate(
                    popularity=Coalesce(
                        Sum("stock__order_entity_stock__count"),
                        0
                    )
                ),
                key=lambda item: item.popularity
            )
        elif sort_by == "-popularity":
            return sorted(
                queryset.annotate(
                    popularity=Coalesce(
                        Sum("stock__order_entity_stock__count"),
                        0
                    )
                ),
                key=lambda item: item.popularity,
                reverse=True
            )
        elif sort_by == "review":
            return sorted(
                queryset.annotate(
                    reviews=Coalesce(
                        Count("user_product_view"),
                        0
                    )
                ),
                key=lambda item: item.reviews
            )
        elif sort_by == "-review":
            return sorted(
                queryset.annotate(
                    reviews=Coalesce(
                        Count("user_product_view"),
                        0
                    )
                ),
                key=lambda item: item.reviews,
                reverse=True
            )
        elif sort_by == "novelty":
            return queryset.order_by("created_at")
        elif sort_by == "-novelty":
            return queryset.order_by("-created_at")
        return sorted(
            queryset,
            key=lambda item: item.discount["price"]
        )

    class AttributeDict(TypedDict):
        id: int
        title: str
        type: str
        values: Set[str]

    def _get_attributes(self) -> List[AttributeDict]:
        """Получение списка атрибутов со значениями, соответствующих данной категории

        :return: Список атрибутов
        :rtype: List[AttributeDict]
        """
        attr_values: list = list(models.AttributeValue.objects.only(
            "attribute__id", "attribute__title", "attribute__type", "value"
        ).filter(
            attribute__category__id=self.query_params["category"]
        ).values(
            "attribute__id", "attribute__title", "attribute__type", "value"
        ))
        attr_values = sorted(
            attr_values, key=lambda item: item["attribute__id"]
        )
        result: list = []
        current_id: int = 0
        for item in attr_values:
            idx: int = item["attribute__id"]
            title: str = item["attribute__title"]
            type: str = item["attribute__type"]
            value: str = item["value"]
            if value == "None":
                continue
            if idx == current_id:
                result[-1]["values"].add(value)
            else:
                result.append(
                    {
                        "id": idx,
                        "title": title,
                        "type": type,
                        "values": set((value,))
                    }
                )
                current_id = idx
        return sorted(result, key=lambda item: item["title"])

    def _get_categories(self) -> List[Optional[int]]:
        """Метод возвращает список категорий: родительской и его дочерних

        :return: Список категорий
        :rtype: List[Optional[int]]
        """
        result: List[Optional[int]] = []
        category_id: int = (
            int(self.query_params["category"])
            if self.query_params.get("category", "").isdigit()
            else 0
        )
        try:
            category: models.Category = models.Category.objects\
                                                       .get(id=category_id)
        except models.Category.DoesNotExist:
            return result
        self.context["category_title"] = category.title
        result.append(category_id)
        result += [
            item[0]
            for item
            in models.Category.objects.only("id")
                              .filter(parent_id=category_id)
                              .values_list("id")
        ]
        if category.parent_id is not None:
            self.context["parent_category_id"] = \
                models.Category.objects.only("id")\
                                       .get(id=category.parent_id).id
            self.context["parent_category_title"] = \
                models.Category.objects.only("title")\
                                       .get(id=category.parent_id).title
        return result

    def _get_prices_shops(self,
                          products: QuerySet[models.Product]) -> Dict[int, Decimal]:
        """Метод устанавливает значения минимальной и максимальной цены,
        списка применимых магазинов для выбранного набора продуктов

        :param products: Список продуктов
        :type products: QuerySet[Product]
        :return: Словарь индексов продуктов со стоимостями
        :rtype: Dict[int, Decimal]
        """
        self.context["shops"] = \
            list(
                Shop.objects.only("id", "name").filter(
                    Q(stock__count__gt=0) &
                    Q(stock__product__in=products)
                ).distinct().order_by("name")
            )
        prices: Dict[int, Decimal] = {
            item.id: item.discount["price"]
            for item
            in products
        }

        self.context["min_price"] = int(min(prices.values()))
        self.context["max_price"] = int(max(prices.values()))

        return prices

    def _get_base_filters(self, prices: Dict[int, Decimal]) -> Q:
        """Функция полуения не зависящих от категории фильтров

        :param prices: Список всех цен на товары
        :type prices: Dict[int, Decimal]
        :return: Фильтр для QuerySet
        :rtype: Q
        """
        result: Q = Q()
        # Фильтр по цене
        if "price" in self.query_params:
            try:
                min_price, max_price = \
                    tuple(
                        map(Decimal, self.query_params["price"].split(sep=';'))
                    )
            except ValueError:
                min_price = self.context["min_price"]
                max_price = self.context["max_price"]
            if (min_price != self.context["min_price"] or
                    max_price != self.context["max_price"]):
                filtered_by_price: List[Optional[int]] = [
                    idx for idx, price in prices.items()
                    if (min_price <= price <= max_price)
                ]

                self.context["filter_min_price"] = int(min_price)
                self.context["filter_max_price"] = int(max_price)

                if filtered_by_price:
                    result &= Q(id__in=filtered_by_price)
        # Фильтр по названию
        if "title" in self.query_params:
            result &= Q(title__icontains=self.query_params["title"])
            self.context["title"] = self.query_params["title"]
        # Фильтр по магазину
        if "shop" in self.query_params:
            self.query_params["shop"] = list(
                map(int, self.query_params["shop"])
            )
            result &= Q(stock__shop__id__in=self.query_params["shop"])
            self.context['selected_shops'] = self.query_params["shop"]
        return result

    def _get_attr_filters(self) -> List[Q]:
        """Функия получения фильтра по аттрибутам, связанным с категорией

        :return: Список фильтров по аттрибутам
        :rtype: List[Q]
        """
        result: List[Q] = []
        self.context["attr_filter"] = {}
        for attr in self.query_params.keys():
            if attr.startswith("attr_"):
                _, type_, id_ = tuple(attr.split(sep="_"))
                self.context["attr_filter"][int(id_)] = self.query_params[attr]
                if type_ == "t":
                    result.append(
                        Q(
                            attribute__id=int(id_),
                            value__icontains=self.query_params[attr]
                        )
                    )
                elif type_ == "s":
                    result.append(
                        Q(
                            attribute__id=int(id_),
                            value=self.query_params[attr]
                        )
                    )
                elif type_ == "c":
                    result.append(
                        Q(
                            attribute__id=int(id_),
                            value="Yes"
                        )
                    )
        return result

    def get_queryset(self):
        # Строка-идентификатор для поиска кэша
        # конкретного набора (по параметрам)
        cache_suffix_params = self.query_params.copy()
        cache_suffix_params.update({'sort_by': self.sort_by})
        cache_suffix = urlencode(cache_suffix_params)
        # Если есть кэш данного набора, то возвращаем его
        product_list_cache = cache.get(
            f'product_list_set_{cache_suffix}',
            default=None
        )
        context_cache = cache.get(
            f'product_list_context_{cache_suffix}',
            default=None
        )

        if product_list_cache is not None and context_cache is not None:
            self.context = context_cache.copy()
            return product_list_cache
        # Если кэша не найдено
        collected_filter: Q = Q(total_count__gt=0)
        if "query" in self.query_params:
            collected_filter &= Q(title__icontains=self.query_params["query"])
            self.context["query"] = self.query_params["query"]
        else:
            categories: List[int] = self._get_categories()
            if categories:
                collected_filter &= Q(category__id__in=categories)
        result: QuerySet = (models.Product.objects.annotate(
            total_count=Sum("stock__count")
        ).filter(collected_filter))
        # Здесь мы получили набор продуктов соответствующий
        # выбранной категории или строке поиска
        prices: Dict[int, Decimal] = self._get_prices_shops(result)
        result = result.filter(self._get_base_filters(prices))
        # Здесь мы получили объекты отфильтрованные по базовому набору
        # фильтров
        if "category" in self.query_params:
            for filter in self._get_attr_filters():
                result = result.filter(
                    product_item__in=models.AttributeValue.objects.filter(
                        filter
                    )
                )
        result = self._get_sorted_list(result, self.sort_by)
        # Формируем кэш данного набора параметров
        product_list_cache_time_setting: Settings = \
            Settings.objects.filter(name="product_list_cache_time").first()
        product_list_cache_time = (
            int(product_list_cache_time_setting.value)
            if product_list_cache_time_setting
            else DEFAULT_CACHE_TIME
        )
        cache.set(
            f'product_list_set_{cache_suffix}',
            result,
            product_list_cache_time
        )
        cache.set(
            f'product_list_context_{cache_suffix}',
            self.context,
            product_list_cache_time
        )
        return result

    def get(self, request, *args, **kwargs):
        self.query_params.update({**request.GET.dict()})
        if "shop" in self.query_params:
            self.query_params["shop"] = request.GET.getlist("shop")
        self.context: Dict[str, Any] = {}
        self.sort_by: str = self.query_params.pop("sort_by", "price")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        url: str = reverse("product:list")
        # Если пришел post запрос, то это из строки поиска или
        # из фильтра по параметрам
        self.query_params.update({**request.POST.dict()})
        # Если из строки поика, то сразу переходим к поиску
        if "query" in self.query_params:
            return redirect(
                url + "?query=%s" % self.query_params["query"]
            )
        # Если из фильтров по аттрибуатм, то удаляем лишние и
        # получаем необходимые
        if "shop" in self.query_params:
            self.query_params["shop"] = request.POST.getlist("shop")
        for name in tuple(self.query_params.keys()):
            if (
                    name == "csrfmiddlewaretoken" or
                    self.query_params[name] == "" or
                    name == "page"
            ):
                del self.query_params[name]
        # Восстанавливаем значение поиска или категории, если есть
        if "category" in request.GET:
            self.query_params["category"] = request.GET["category"]
        if "query" in request.GET:
            self.query_params["query"] = request.GET["query"]
        return redirect(
            url + "?%s" % urlencode(self.query_params, True)
        )

    def get_context_data(self, **kwargs):
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update({**self.context})
        if 'category' in self.query_params:
            context['attributes'] = self._get_attributes()
        context['base_url'] = urlencode(self.query_params, True)
        return context


class ProductDetailView(FormMixin, DetailView):
    """
       Представление страницы product.html

       - детальное описание товара;
       - форма для отзыва;
   """

    model = models.Product
    template_name = "product/product.html"
    context_object_name = "product"
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        product_on_page = self.get_object()
        context["images"] = \
            models.ProductImage.get_product_pics(product_on_page)
        context["attributes"] =\
            models.AttributeValue.get_all_attributes_of_product(product_on_page)
        context["comments"] = \
            models.ProductReview.get_comments(product_on_page)
        context["stocks"] = models.Stock.get_products_in_stock(product_on_page)

        get_product_detail_view.send(sender=self.__class__,
                                     user=self.request.user,
                                     product=product_on_page.id)

        return context

    def post(self, request, *args, **kwargs):
        product_item = self.get_object()
        post_data = request.POST.copy()

        post_data["product"] = product_item
        post_data["user"] = self.request.user
        form = ProductReviewForm(post_data)
        if form.is_valid():
            form.save()
        if "rating" in post_data:
            avg_rating = models.ProductReview.objects.filter(
                product=product_item
            ).aggregate(
                avg=Avg("rating", filter=F("rating"))
            )
            product_item.rating = round(avg_rating["avg"])
            product_item.save()

        return HttpResponseRedirect(
            reverse(
                "product:detail",
                kwargs={
                    "pk": product_item.id,
                }
            )
        )
