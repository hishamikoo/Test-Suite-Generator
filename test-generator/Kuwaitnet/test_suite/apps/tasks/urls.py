from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# We have a useful decorator, called login_required
# Check now when you go to / it will show another error
# saying we don't have accounts/login
# let's use admin login page for now


urlpatterns = [
    path("", login_required(views.intro), name="intro"),
    path("s/<code>/", views.show_suite, name="show_suite"),
    path("s/<code>/<password>", views.password_form, name = "password_form"),
    path("s/<code>?password=<password>", views.protected_suite, name = "protected_suite"),
    path("display_suite/", views.display_suite, name="display_suite"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)