
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secret-chambers/', admin.site.urls),
    path('skyfinance/', include('skyfinance_app.urls'))
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
