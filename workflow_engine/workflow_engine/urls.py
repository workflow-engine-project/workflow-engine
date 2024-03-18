from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project_apps.api.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="워크플로우 및 스케줄링 API",  # API 타이틀
        default_version='v1',  # API 버전
        description="워크플로우 관리 및 작업 스케줄링을 위한 통합 API. 이 API를 통해 사용자는 복잡한 작업 흐름을 구성하고, 스케줄링할 수 있으며, 실행 상태를 모니터링할 수 있습니다. API는 다양한 워크플로우 구성, 작업 실행기능을 제공합니다.",
        terms_of_service="https://www.yourcompany.com/policy",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"), 
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project_apps.api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
