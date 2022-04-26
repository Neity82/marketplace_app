from typing import Tuple, List


def avatar_directory_path(instance, filename) -> str:
    """Функция формирует путь для размещения фотографии/аватара пользователя"""

    return 'avatar/user_{id}/{filename}'.format(id=instance.id, filename=filename)


def full_name_analysis(name: List[str]) -> Tuple[str, str, str]:
    """
    Функция получает на вход полное имя клиента,
    возвращает фамилию, имя и отчество
    """

    last_name, first_name, middle_name = str(), str(), str()
    if len(name) == 3:
        last_name, first_name, middle_name = name[0], name[1], name[2]
    elif len(name) == 2:
        last_name, first_name = name[0], name[1]
    else:
        last_name = name[0]

    return last_name, first_name, middle_name
