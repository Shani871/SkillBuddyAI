

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from SkillBuddyAI.view import home, signup, login_user, logout_user, profile
from Task import urls

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page
    path('', home, name='home'),  # Home page
    path('signup/', signup, name='signup'),  # Signup page
    path('login/', login_user, name='login'),  # Login page
    path('logout/', logout_user, name='logout'),  # Logout page
    path('profile/', profile, name='profile'),  # Profile page
    path('tasks/', include('Task.urls')),
path('', include('face_recognition.urls')),
    path('api/', include('chatbot.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])