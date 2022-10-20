from rest_framework.routers import SimpleRouter

from django.urls import path, re_path
from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"users", views.UserViewSet)

urlpatterns = [
    path("artist/<int:id>", views.DeezerArtistView.as_view()),
    path("album/<int:id>", views.DeezerAlbumView.as_view()),
    re_path(r"search/$", views.DeezerSongView.as_view()),
]


urlpatterns += r.urls
