from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoices')

schema_view = get_schema_view(
    openapi.Info(
        title="Invoice_Django_API",
        default_version='v1.0',
        description="Documentation for the Django Invoices API",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.as_view(), name='swagger-docs'), 
]