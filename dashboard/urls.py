from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

    # ======================
    # User Management
    # ======================

    path(
        "users/",
        views.user_list,
        name="user_list"
    ),

    path(
        "users/add/",
        views.add_user,
        name="add_user"
    ),

    path(
        "users/edit/<int:user_id>/",
        views.edit_user,
        name="edit_user"
    ),

    path(
        "users/delete/<int:user_id>/",
        views.delete_user,
        name="delete_user"
    ),
    
    path(
        "orders/",
        views.order_list,
        name="dashboard_orders"
    ),
    
    path(
        "orders/<int:order_id>/",
        views.order_detail_admin,
        name="order_detail_admin"
    ),
    path(
        "consultations/",
        views.consultation_list,
        name="dashboard_consultations"
    ),
    
    path(
        "reports/",
        views.reports,
        name="reports"
    ),
    
    path(
        "settings/",
        views.settings,
        name="settings"
    ),
    
    path(
        "search/",
        views.global_search,
        name="global_search"
    ),
    
    path(
        "logout/",
        views.admin_logout,
        name="admin_logout"
    ),
]