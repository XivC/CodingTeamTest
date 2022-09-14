from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Prefetch, Count, Q, F
from codeteamtask import settings

from restaurant import models
from restaurant import serializers


@api_view(['GET'])
def foods_handler(request):

    if settings.DEBUG:
        load_test_data()

    if request.method == 'GET':
        categories = models.FoodCategory.objects.all(
        ).prefetch_related(
            Prefetch('food', queryset=models.Food.objects.exclude(is_publish=False))
        ).annotate(
            cnt=Count('food')
        ).annotate(
            cnt_unpub=Count('food', filter=Q(food__is_publish=False))
        ).filter(
            cnt__gt=F('cnt_unpub')
        )

        serializer = serializers.FoodListSerializer(categories, many=True)
        return Response(serializer.data)


def load_test_data():

    # заполняем тестовые данные
    from restaurant import models

    drinks = models.FoodCategory(name_ru='напитки')
    soups = models.FoodCategory(name_ru='супы')
    main_courses = models.FoodCategory(name_ru='вторые блюда')
    desserts = models.FoodCategory(name_ru='десерты')
    alcohols = models.FoodCategory(name_ru='алкоголь')

    drink1 = models.Food(name_ru='квас', category=drinks, code=1, cost=100)
    drink2 = models.Food(name_ru='кисель', category=drinks, code=2, cost=120)
    drink3 = models.Food(name_ru='чай', category=drinks, code=3, cost=150)

    soup1 = models.Food(name_ru='гороховый', category=soups, code=5, cost=110)
    soup2 = models.Food(name_ru='борщ', category=soups, code=6, cost=120)

    dessert1 = models.Food(name_ru='кекс', category=desserts, code=7, cost=130)
    dessert2 = models.Food(name_ru='чизкейк', category=desserts, code=8, cost=150, is_publish=False)
    dessert3 = models.Food(name_ru='штрудель', category=desserts, code=9, cost=112)

    alcohol1 = models.Food(name_ru='пиво', category=alcohols, code=10, cost=220, is_publish=False)
    alcohol2 = models.Food(name_ru='вино', category=alcohols, code=11, cost=520, is_publish=False)

    drink4 = models.Food(name_ru='лимонад', category=drinks, code=4, cost=400)
    categories = [drinks, soups, main_courses, desserts, alcohols]
    foods = [drink1, drink2, drink3, soup1, soup2, dessert1, dessert2, dessert3, alcohol1, alcohol2, drink4]
    for cat in categories:
        try:
            cat.save()
        except Exception:
            continue

    for food in foods:
        try:
            food.save()
        except Exception:
            continue

    try:
        drink4.additional.add(dessert1)
    except ValueError:
        pass
