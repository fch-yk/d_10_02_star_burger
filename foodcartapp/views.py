from django.http import JsonResponse
from django.templatetags.static import static
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError


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


def validate_order_card(order_card):
    sections = (
        {'key': 'address', 'valid_class': str},
        {'key': 'firstname', 'valid_class': str},
        {'key': 'lastname', 'valid_class': str},
        {'key': 'phonenumber', 'valid_class': str},
        {'key': 'products', 'valid_class': list},
    )
    for section in sections:
        order_clause = order_card.get(section['key'], section['valid_class'])
        if not isinstance(order_clause, section['valid_class']):
            raise ValidationError(
                f'{section["key"]} key not presented '
                f'or not {section["valid_class"]}'
            )

        if not order_clause:
            raise ValidationError(f'{section["key"]} cannot be empty')

        validate_international_phonenumber(order_card['phonenumber'])


@ api_view(['POST'])
def register_order(request):
    order_card = request.data
    try:
        validate_order_card(order_card)
        products = []
        for item_card in order_card['products']:
            products.append(
                {
                    'product': Product.objects.get(id=item_card['product']),
                    'quantity': item_card['quantity']
                }
            )

        order = Order.objects.create(
            address=order_card['address'],
            first_name=order_card['firstname'],
            last_name=order_card['lastname'],
            mobile_number=order_card['phonenumber'],
        )
        for product_card in products:
            OrderItem.objects.create(
                order=order,
                product=product_card['product'],
                quantity=product_card['quantity'],
            )
    except (ValidationError) as error:
        return Response(
            {'error': error},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    except (Product.DoesNotExist) as error:
        return Response(
            {'error': f'{str(error)} id: {item_card["product"]}'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )

    return Response({})
