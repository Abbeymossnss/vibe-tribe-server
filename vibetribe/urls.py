from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from tribeapi.views import EventView, TribeUserViewSet
from tribeapi.views import TagView
from tribeapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)

# Register TribeUserViewSet with a URL path
router.register(r'tribe_users', TribeUserViewSet, basename='tribe_user')  # Specify 'basename'
router.register(r'events', EventView, 'event')
router.register(r'tags', TagView, 'tag')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
