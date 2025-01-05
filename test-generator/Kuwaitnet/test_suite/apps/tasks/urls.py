from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView


from . import views

# We have a useful decorator, called login_required
# Check now when you go to / it will show another error
# saying we don't have accounts/login
# let's use admin login page for now


urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),  # Redirect root to /generate/
    path('home/', views.home, name = "home"),
    path("generate/", login_required(views.generate), name="generate"),
    path("s/<code>/", views.show_suite, name="show_suite"),
    path("s/<code>/<password>", views.password_form, name = "password_form"),
    path("s/<code>?password=<password>", views.protected_suite, name = "protected_suite"),
    path("display_suite/", views.display_suite, name="display_suite"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-success/', TemplateView.as_view(template_name='logout_success.html'), name='logout_success'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)