from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from apps.datos.views import CustomUserViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'transactions', TransactionViewSet)

schema_view = get_swagger_view(title='osw4l api 2.0')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('', schema_view),
    path('api/', include(router.urls)),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

