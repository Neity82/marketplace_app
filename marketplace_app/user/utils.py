def avatar_directory_path(instance, filename) -> str:
    """Функция формирует путь для размещения фотографии/аватара пользователя"""
    return 'avatar/user_{id}/{filename}'.format(id=instance.id, filename=filename)
