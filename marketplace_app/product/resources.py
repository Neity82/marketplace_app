import os
import shutil

from import_export import resources

from marketplace_app.settings import IMPORT_FILE_ROOT
from product.models import Stock, Product


class ProductResource(resources.ModelResource):
    """
    Класс, в котором описано, как модель Product
    будет импортирована в панели администратора
    """

    class Meta:
        model = Product
        skip_unchanged = True


class StockResource(resources.ModelResource):
    """
        Класс, в котором описано, как модель Stock
        будет импортирована в панели администратора
    """

    class Meta:
        model = Stock
        skip_unchanged = True

    # def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
    #     file_name = kwargs["file_name"]
    #     src = os.path.join(IMPORT_FILE_ROOT, "new", file_name)
    #     if result.has_errors():
    #         # shutil.move(path, 'errors')
    #         pass
    #     if dry_run is False:
    #         if not result.has_errors():
    #             dst = os.path.join(IMPORT_FILE_ROOT, "executed", file_name)
    #             shutil.move(src, dst)









