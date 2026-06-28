from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from .forms import RegisterForm
from orders.models import Order

def profile_view(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')[:5]

    return render(
        request,
        'accounts/profile.html',
        {
            'orders': orders,
            'user': request.user
        }
    )

def register(request):

    form = RegisterForm(
        request.POST or None
    )

    if form.is_valid():

        user = form.save()

        login(
            request,
            user
        )

        return redirect(
            'product_list'
        )

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'product_list'
            )

    return render(
        request,
        'accounts/login.html'
    )

def user_logout(request):

    logout(request)

    return redirect(
        'login'
    )

def profile(request):

    return render(
        request,
        'accounts/profile.html'
    )