
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secret-chambers/', admin.site.urls),
    path('skyfinance/', include('skyfinance_app.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
