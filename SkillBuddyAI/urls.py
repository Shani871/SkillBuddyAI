from django import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from SkillBuddyAI.view import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])