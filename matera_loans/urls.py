"""
URL configuration for matera_loans project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.views import UserCreate, LoanViewSet, PaymentViewSet

router = DefaultRouter()
router.register("loans", LoanViewSet, basename="loans")
router.register("payments", PaymentViewSet, basename="payments")

schema_view = get_schema_view(
    openapi.Info(
        title="Matera Loans API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,))

urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path('login/', obtain_auth_token, name='login'),
    path("", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
