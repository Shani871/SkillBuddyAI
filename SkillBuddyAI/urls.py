from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SkillBuddyAI.view import home, signup, login_user, TaskManager

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login_user'),
    path('TaskManager/', TaskManager, name='TaskManager'),
 path("chatbot/", include("chatbot.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])