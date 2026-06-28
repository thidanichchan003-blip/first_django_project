from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from orders.models import Order
from consultation.models import Consultation, Notification
from accounts.models import UserProfile
from products.models import Product, Category
from django.db.models import Sum, Count
from orders.models import Order, OrderItem
from settings_app.models import SiteSetting
from settings_app.forms import SiteSettingForm
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect


# ===========================
# Dashboard
# ===========================

@login_required
def dashboard(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_consultations = Consultation.objects.count()

    pending_orders = Order.objects.filter(
        status="Pending"
    ).count()

    revenue = Order.objects.aggregate(
        total=Sum("total_price")
    )["total"] or 0

    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:5]

    recent_consultations = Consultation.objects.order_by(
        "-created_at"
    )[:5]

    low_stock = Product.objects.filter(
        stock__lte=5
    )

    context = {

        "notification_count": notification_count,

        "total_users": total_users,

        "total_products": total_products,

        "total_orders": total_orders,

        "total_consultations": total_consultations,

        "pending_orders": pending_orders,

        "total_revenue": revenue,

        "recent_orders": recent_orders,

        "recent_consultations": recent_consultations,

        "low_stock": low_stock,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# ===========================
# Notifications
# ===========================

@login_required
def notifications(request):

    Notification.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )

    notifications = Notification.objects.order_by(
        "-created_at"
    )

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    return render(
        request,
        "dashboard/notifications.html",
        {
            "notifications": notifications,
            "notification_count": notification_count,
        }
    )


# ===========================
# User List
# ===========================

@login_required
def user_list(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    users = User.objects.all().order_by("-date_joined")
    q = request.GET.get("q")
    if q:
        users = users.filter(
            username__icontains=q
        )

    return render(
        request,
        "dashboard/users/user_list.html",
        {
            "users": users,
            "notification_count": notification_count,
        }
    )


@login_required
def add_user(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    if request.method == "POST":

        username = request.POST.get("username")

        email = request.POST.get("email")

        password = request.POST.get("password")

        role = request.POST.get("role")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )

        return redirect("user_list")

    return render(
        request,
        "dashboard/users/add_user.html",
        {
            "notification_count": notification_count,
        }
    )
    
    
# ===========================
# Edit User
# ===========================

@login_required
def edit_user(request, user_id):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    user = get_object_or_404(
        User,
        id=user_id
    )

    profile, created = UserProfile.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        user.username = request.POST.get("username")

        user.email = request.POST.get("email")

        user.is_active = (
            request.POST.get("status") == "active"
        )

        profile.role = request.POST.get("role")

        user.save()

        profile.save()

        return redirect("user_list")

    return render(
        request,
        "dashboard/users/edit_user.html",
        {
            "user": user,
            "profile": profile,
            "notification_count": notification_count,
        }
    )


# ===========================
# Delete User
# ===========================

@login_required
def delete_user(request, user_id):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    user = get_object_or_404(
        User,
        id=user_id
    )

    # Prevent deleting your own account
    if user == request.user:

        return redirect("user_list")

    if request.method == "POST":

        user.delete()

        return redirect("user_list")

    return render(
        request,
        "dashboard/users/delete_user.html",
        {
            "user": user,
            "notification_count": notification_count,
        }
    )


from django.db.models import Sum


@login_required
def order_list(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    orders = Order.objects.all().order_by(
        "-created_at"
    )

    pending_orders = Order.objects.filter(
        status="Pending"
    ).count()

    completed_orders = Order.objects.filter(
        status="Completed"
    ).count()

    total_revenue = Order.objects.filter(
        status="Completed"
    ).aggregate(
        total=Sum("total_price")
    )["total"] or 0

    return render(

        request,

        "dashboard/orders/order_list.html",

        {

            "orders": orders,

            "pending_orders": pending_orders,

            "completed_orders": completed_orders,

            "total_revenue": total_revenue,

            "notification_count": notification_count,

        }

    )    
    
    
    
@login_required
def order_detail_admin(request, order_id):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        order.status = request.POST.get("status")

        order.save()

        Notification.objects.create(

            title="Order Status Updated",

            message=f"Order #{order.id} has been updated to {order.status}.",

            notification_type="order",

            link=f"/dashboard/orders/{order.id}/"

        )

        return redirect(
            "order_detail_admin",
            order_id=order.id
        )

    return render(
        request,
        "dashboard/orders/order_detail.html",
        {
            "order": order,
            "notification_count": notification_count,
        }
    )
    
    
    
@login_required
def consultation_list(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    consultations = Consultation.objects.select_related(
        "user"
    ).order_by("-created_at")

    open_consultations = Consultation.objects.filter(
        status="Open"
    ).count()

    closed_consultations = Consultation.objects.filter(
        status="Closed"
    ).count()

    return render(

        request,

        "dashboard/consultations/consultation_list.html",

        {

            "consultations": consultations,

            "open_consultations": open_consultations,

            "closed_consultations": closed_consultations,

            "notification_count": notification_count,

        }

    )
    
    
@login_required
def reports(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    total_revenue = Order.objects.filter(
        status="Completed"
    ).aggregate(
        total=Sum("total_price")
    )["total"] or 0

    total_orders = Order.objects.count()

    total_customers = User.objects.count()

    total_products_sold = OrderItem.objects.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    top_products = (
        OrderItem.objects
        .values(
            "product__name"
        )
        .annotate(
            sold=Sum("quantity")
        )
        .order_by("-sold")[:5]
    )

    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:10]

    return render(

        request,

        "dashboard/reports/report.html",

        {

            "notification_count": notification_count,

            "total_revenue": total_revenue,

            "total_orders": total_orders,

            "total_customers": total_customers,

            "total_products_sold": total_products_sold,

            "top_products": top_products,

            "recent_orders": recent_orders,

        }

    )
    
    
@login_required
def settings(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    setting, created = SiteSetting.objects.get_or_create(id=1)

    form = SiteSettingForm(
        request.POST or None,
        request.FILES or None,
        instance=setting
    )

    if form.is_valid():
        form.save()
        return redirect("settings")

    return render(
        request,
        "dashboard/settings/settings.html",
        {
            "form": form,
            "notification_count": notification_count,
        }
    )
    
@login_required
def global_search(request):

    query = request.GET.get("q", "")

    users = []
    products = []
    orders = []
    consultations = []

    if query:

        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

        products = Product.objects.filter(
            name__icontains=query
        )

        orders = Order.objects.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query)
        )

        consultations = Consultation.objects.filter(
            Q(user__username__icontains=query) |
            Q(status__icontains=query)
        )

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    return render(

        request,

        "dashboard/search_results.html",

        {

            "query": query,

            "users": users,

            "products": products,

            "orders": orders,

            "consultations": consultations,

            "notification_count": notification_count,

        }

    )
    
@login_required
def admin_logout(request):

    logout(request)

    return redirect("login")