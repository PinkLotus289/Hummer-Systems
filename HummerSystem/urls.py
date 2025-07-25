
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('auth/', include('users.urls')),
    path('ui/phone_form/', TemplateView.as_view(template_name='users/phone_form.html'), name='phone-form'),
    path('ui/profile/', TemplateView.as_view(template_name='users/profile.html'), name='profile-ui'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
