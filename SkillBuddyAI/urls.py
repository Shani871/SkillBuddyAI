

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from SkillBuddyAI.view import home, signup, login_user, logout_user, profile, about, blog, contact, portfolio
from chatbot.views import chatbot_view

from face.views import video_feed

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page
    path('', home, name='home'),  # Home page
    path('signup/', signup, name='signup'),  # Signup page
    path('login/', login_user, name='login'),  # Login page
    path('logout/', logout_user, name='logout'),  # Logout page
    path('profile/', profile, name='profile'),  # Profile page
      # Home page
    path('video_feed/', video_feed, name='video_feed'),
    path('chatbot/', chatbot_view, name='chatbot_view'),
    path('about/',about, name='about'),
    path('blog/',blog ,name='blog'),
    path('contact/',contact,name='contact'),
    path('portfolio/',portfolio,name='portfolio'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])