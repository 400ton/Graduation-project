from diary.models import Diary


def base_view(request):
    """
    Базовое представление для получения общего количества записей,
    находящихся на модерации.

    Функция получает количество записей со статусом "moderation" и
    возвращает это значение в виде контекста, который можно использовать
    в шаблонах для отображения счетчика модераций.

    Аргументы:
            request (HttpRequest): Объект HTTP-запроса.

    Возвращает:
            dict: Словарь с ключом 'moderation_count', содержащий количество записей,
            находящихся на модерации.
    """
    moderation_count = Diary.objects.filter(status='moderation').count()
    return {
        'moderation_count': moderation_count,
    }
