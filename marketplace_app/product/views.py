from django.db.models import QuerySet, Sum
from django.http.request import HttpRequest, QueryDict
from django.views import generic
from django.shortcuts import redirect, render
from .models import Category, Product


def index(request, *args, **kwargs):
    return render(request, 'product/index.html', {})


def compare(request, *args, **kwargs):
    return render(request, 'product/compare.html', {})


def product(request, *args, **kwargs):
    return render(request, 'product/product.html', {})


class ProductListView(generic.ListView):
    template_name = "product/catalog.html"
    paginate_by = 8
    context_object_name = "products"

    def get_queryset(self):
        result: QuerySet = (Product.objects.annotate(total_count=Sum("stock"))
                            .filter(total_count__gt=0))
        query: str = (
            QueryDict(self.request.GET.urlencode()).dict().get("query", "")
        )
        if query:
            return result.filter(title__icontains=query)
        category: int = (
            int(self.request.GET.dict().get("category", ""))
            if self.request.GET.dict().get("category", "").isdigit()
            else 0
        )
        if not Category.objects.filter(id=category):
            category = 0
        if category:
            categories_list: list = [category]
            for subcategory in Category.objects.filter(parent_id=category):
                subcategory_id: int = subcategory.id
                categories_list.append(subcategory_id)
                for subsubcategory in (
                    Category.objects.filter(parent_id=subcategory.id)
                ):
                    categories_list.append(subsubcategory.id)
            result = result.filter(category__id__in=categories_list)
        result = result.order_by("sort_index", "title", "id")
        return result

    def post(self, request: HttpRequest, *args, **kwargs):
        search_query = QueryDict(request.POST.urlencode()).dict()["query"]
        return redirect(f"/catalog/?query={search_query}")

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
