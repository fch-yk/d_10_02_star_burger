from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_card = request.data
    products = order_card.get('products', None)
    if not isinstance(products, list):
        content = {'error': 'product key not presented or not list'}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not products:
        content = {'error': 'products list cannot be empty'}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

    order = Order.objects.create(
        address=order_card['address'],
        first_name=order_card['firstname'],
        last_name=order_card['lastname'],
        mobile_number=order_card['phonenumber'],
    )
    for item_card in products:
        OrderItem.objects.create(
            order=order,
            product=Product.objects.get(id=item_card['product']),
            quantity=item_card['quantity'],
        )
    return Response({})
