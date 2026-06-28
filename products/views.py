from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm, CategoryForm

from cart.models import CartItem


# ==========================
# Product List
# ==========================

def product_list(request):

    products = Product.objects.all()

    q = request.GET.get("q")

    if q:
        products = products.filter(
            name__icontains=q
        )

    categories = Category.objects.all()

    category_id = request.GET.get("category")

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    for product in products:

        product.cart_qty = 0

        if request.user.is_authenticated:

            item = CartItem.objects.filter(
                user=request.user,
                product=product
            ).first()

            if item:

                product.cart_qty = item.quantity

    return render(
        request,
        "products/list.html",
        {
            "products": products,
            "categories": categories,
        }
    )


# ==========================
# Add Product
# ==========================

@login_required
def add_product(request):

    form = ProductForm(

        request.POST or None,

        request.FILES or None

    )

    if form.is_valid():

        form.save()

        return redirect("product_list")

    return render(

        request,

        "products/form.html",

        {

            "form": form,

            "title": "Add Product",

            "button": "Add Product",

        }

    )


# ==========================
# Edit Product
# ==========================

@login_required
def edit_product(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    form = ProductForm(

        request.POST or None,

        request.FILES or None,

        instance=product

    )

    if form.is_valid():

        form.save()

        return redirect("product_list")

    return render(

        request,

        "products/form.html",

        {

            "form": form,

            "title": "Edit Product",

            "button": "Save Changes",

            "product": product,

        }

    )


# ==========================
# Delete Product
# ==========================

@login_required
def delete_product(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    if request.method == "POST":

        product.delete()

        return redirect("product_list")

    return render(

        request,

        "products/delete_confirm.html",

        {

            "product": product

        }

    )


# ==========================
# Product Detail
# ==========================

def product_detail(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    return render(

        request,

        "products/detail.html",

        {

            "product": product

        }

    )


# ==========================
# Category List
# ==========================

@login_required
def category_list(request):

    categories = Category.objects.all()

    return render(

        request,

        "products/category_list.html",

        {

            "categories": categories

        }

    )


# ==========================
# Add Category
# ==========================

@login_required
def category_create(request):

    form = CategoryForm(

        request.POST or None

    )

    if form.is_valid():

        form.save()

        return redirect("category_list")

    return render(

        request,

        "products/category_form.html",

        {

            "form": form

        }

    )


# ==========================
# Edit Category
# ==========================

@login_required
def category_update(request, id):

    category = get_object_or_404(

        Category,

        id=id

    )

    form = CategoryForm(

        request.POST or None,

        instance=category

    )

    if form.is_valid():

        form.save()

        return redirect("category_list")

    return render(

        request,

        "products/category_form.html",

        {

            "form": form

        }

    )


# ==========================
# Delete Category
# ==========================

@login_required
def category_delete(request, id):

    category = get_object_or_404(

        Category,

        id=id

    )

    if request.method == "POST":

        category.delete()

        return redirect("category_list")

    return render(

        request,

        "products/delete_confirm.html",

        {

            "category": category

        }

    )