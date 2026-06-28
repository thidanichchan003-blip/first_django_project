
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from django.views.generic import RedirectView

urlpatterns = [
    path(
        '',
        RedirectView.as_view(url='/accounts/login/', permanent=False)
    ),
    path("dashboard/", include("dashboard.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('consultation/', include('consultation.urls')),
   
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )