"""
URL configuration for myorg project.

This file defines the main URL routing for the entire project.
It connects app-level URLs, admin panel, and API documentation.

For more information:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

# =====================================================
# IMPORTS
# =====================================================

from django.contrib import admin               # Django admin panel
from django.urls import path, include          # URL routing functions
from rest_framework import permissions         # Permission settings for API access

# Swagger / OpenAPI imports for API documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# =====================================================
# SWAGGER CONFIGURATION
# Generates interactive API documentation
# =====================================================

schema_view = get_schema_view(
    openapi.Info(
        title="TestDB API",                     # Title shown in Swagger UI
        default_version='v1',                   # API version
        description="CRUD API for Department & Employee",  # API description
    ),
    public=True,                                # API is publicly accessible
    permission_classes=(permissions.AllowAny,), # No authentication required
)


# =====================================================
# MAIN URL PATTERNS
# Maps URLs to views or app routes
# =====================================================

urlpatterns = [

    # -------------------------
    # Admin Panel
    # URL: http://127.0.0.1:8000/admin/
    # -------------------------
    path('admin/', admin.site.urls),

    # -------------------------
    # App URLs (INFA app)
    # Includes all routes defined in infa/urls.py
    # Example: /users/, /opportunities/, etc.
    # -------------------------
    path('', include('infa.urls')),

    # -------------------------
    # Swagger API Documentation
    # URL: http://127.0.0.1:8000/swagger/
    # Provides interactive API testing UI
    # -------------------------
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]