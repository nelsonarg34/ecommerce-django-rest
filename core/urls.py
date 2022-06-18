from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('authentication.urls')),
    path('api/product/', include('product.urls')),
    path('api/order/', include('order.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)