import os.path


def category_icon_path(instance, filename) -> str:
    extension = os.path.splitext(filename)
    return "category/{id}-{title}.{extension}".format(
        id=instance.id, title=instance.title, extension=extension
    )


def product_image_path(instance, filename) -> str:
    extension = os.path.splitext(filename)
    return "product/{id}.{extension}".format(
        id=instance.id, extension=extension
    )



