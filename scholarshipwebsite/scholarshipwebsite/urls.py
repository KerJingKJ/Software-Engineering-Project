
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("landingpage.urls")),
    path('', include("login.urls")),
    path('committee/', include("committee.urls")),
    path('reviewer/', include("reviewer.urls")),
    path('student/', include("student.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
