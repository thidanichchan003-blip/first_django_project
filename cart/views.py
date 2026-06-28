from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import CartItem
from products.models import Product



@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if product.stock <= 0:

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'quantity': 0
            })

        return redirect('product_list')

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse({
            'quantity': cart_item.quantity
        })

    return redirect('cart')


@login_required
def cart_view(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:
        total += item.subtotal()

    return render(
        request,
        'cart/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )

@login_required
def remove_from_cart(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect('cart')



@login_required
def increase_quantity(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


@login_required
def decrease_from_product(request, product_id):

    item = CartItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).first()

    quantity = 0

    if item:

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            quantity = item.quantity

        else:
            item.delete()
            quantity = 0

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse({
            'quantity': quantity
        })

    return redirect('product_list')