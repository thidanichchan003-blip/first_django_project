from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from .models import Order
from .models import OrderItem

from consultation.models import Notification

from cart.models import CartItem
from .forms import CheckoutForm


@login_required
def order_list(request):

    orders = Order.objects.filter(
        user=request.user
    )

    return render(
        request,
        'orders/order_list.html',
        {
            'orders': orders
        }
    )


@login_required
def checkout(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    if not cart_items:
        return redirect('cart')

    total = sum(
        item.subtotal()
        for item in cart_items
    )

    if request.method == 'POST':

        form = CheckoutForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            order = Order.objects.create(
                user=request.user,
                total_price=total,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                payment_proof=form.cleaned_data['payment_proof'],
                payment_method='ABA',
                payment_status='Pending'
            )

            for item in cart_items:

                if item.product.stock >= item.quantity:

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                    item.product.stock -= item.quantity
                    item.product.save()

            cart_items.delete()

            Notification.objects.create(

                title="🛒 New Order",

                message=f"{request.user.username} placed Order #{order.id} worth ${order.total_price}",

                notification_type="order",

                link=f"/dashboard/orders/{order.id}/"

            )

            return redirect("order_list")
    else:

        form = CheckoutForm()

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'total': total
        }
    )