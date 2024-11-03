from django.urls import path

# retrieve img
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.users, name="users"),
    path("<int:id>/", views.user_details, name="user_details"),
    path("generate", views.generate_user, name="generate_user"),
    path("referees", views.referees, name="referees"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
