from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from tribeapi.views import register_user, login_user

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]

# # Requests to http://localhost:8000/register will be routed to the register_user function
# path('register', register_user)

# # Requests to http://localhost:8000/login will be routed to the login_user function
# path('login', login_user)
