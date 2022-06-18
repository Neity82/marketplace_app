from import_export import resources
from product.models import Stock, Product


class ProductResource(resources.ModelResource):
    """
    Класс, в котором описано, как модель Product
    будет импортирована в панели администратора
    """

    class Meta:
        model = Product
        skip_unchanged = True

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        print('!!!!!!!!!!!! OK!!!!!!!!!!')


class StockResource(resources.ModelResource):
    """
        Класс, в котором описано, как модель Stock
        будет импортирована в панели администратора
    """

    class Meta:
        model = Stock
        skip_unchanged = True

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if dry_run is False:
            print('!!!!!!!!!!!!!!!')






