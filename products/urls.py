from django.urls import path
from . import views

urlpatterns = [

    # Product

    path(
        "",
        views.product_list,
        name="product_list"
    ),

    path(
        "add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "edit/<int:id>/",
        views.edit_product,
        name="edit_product"
    ),

    path(
        "delete/<int:id>/",
        views.delete_product,
        name="delete_product"
    ),

    path(
        "<int:id>/",
        views.product_detail,
        name="product_detail"
    ),

    # Category

    path(
        "categories/",
        views.category_list,
        name="category_list"
    ),

    path(
        "categories/add/",
        views.category_create,
        name="category_create"
    ),

    path(
        "categories/edit/<int:id>/",
        views.category_update,
        name="category_update"
    ),

    path(
        "categories/delete/<int:id>/",
        views.category_delete,
        name="category_delete"
    ),

]