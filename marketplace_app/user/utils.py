import os


def avatar_directory_path(instance, filename) -> str:
    """Функция формирует путь для размещения фотографии/аватара пользователя"""

    extension = os.path.splitext(filename)
    return "avatar/user_{id}/{extension}".format(
        id=instance.id,
        extension=extension
    )


def full_name_analysis(full_name: str) -> dict:
    """
    Функция получает на вход полное имя клиента,
    возвращает фамилию, имя и отчество
    """

    user_name_data = {}
    if full_name:
        user_name_data_raw = full_name.split()
        user_name_data_raw_len = len(user_name_data_raw)
        if user_name_data_raw_len == 3:
            user_name_data.update(first_name=user_name_data_raw[1])
            user_name_data.update(last_name=user_name_data_raw[0])
            user_name_data.update(middle_name=user_name_data_raw[2])

        elif user_name_data_raw_len == 2:
            user_name_data.update(first_name=user_name_data_raw[1])
            user_name_data.update(last_name=user_name_data_raw[0])

        elif user_name_data_raw_len == 1:
            user_name_data.update(first_name=user_name_data_raw[0])

        elif user_name_data_raw_len > 3:
            user_name_data.update(last_name=user_name_data_raw[0])
            user_name_data.update(middle_name=user_name_data_raw[-1])
            user_name_data.update(first_name=" ".join(user_name_data_raw[1:-1]))
    else:
        user_name_data = full_name
    return user_name_data
