import os
import shutil

from import_export import resources
from import_export_celery.models import ImportJob

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

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if dry_run is False:
            import_job = ImportJob.objects.all().order_by("-id").first()
            import_job_file = str(import_job.file)
            file_name = "_".join(import_job_file.split("/")[-1].split("_")[:-1])
            file_format = import_job_file.split(".")[-1]
            file = ".".join([file_name, file_format])
            src = os.path.join(IMPORT_FILE_ROOT, "new", file)
            if not result.has_errors():
                dst = os.path.join(IMPORT_FILE_ROOT, "executed", file)
                shutil.move(src, dst)
            else:
                dst = os.path.join(IMPORT_FILE_ROOT, "errors", file)
                shutil.move(src, dst)


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
            import_job = ImportJob.objects.all().order_by("-id").first()
            import_job_file = str(import_job.file)
            file_name = "_".join(import_job_file.split("/")[-1].split("_")[:-1])
            file_format = import_job_file.split(".")[-1]
            file = ".".join([file_name, file_format])
            src = os.path.join(IMPORT_FILE_ROOT, "new", file)
            if not result.has_errors():
                dst = os.path.join(IMPORT_FILE_ROOT, "executed", file)
                shutil.move(src, dst)
            else:
                dst = os.path.join(IMPORT_FILE_ROOT, "errors", file)
                shutil.move(src, dst)
