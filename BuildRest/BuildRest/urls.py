from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from building import views


schema_view = get_schema_view(
   openapi.Info(
      title="Django API",
      default_version='v1',
      description="Some description",
      terms_of_service="https://www.domain.com",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/', include('building.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

