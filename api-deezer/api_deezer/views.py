from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api import views
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
import requests
from . import models, serializers
from drf_yasg import openapi

URL_API_DEEZER = "https://api.deezer.com/"
URL_API_DEEZER_ARTIST = URL_API_DEEZER + "artist/"
URL_API_DEEZER_ALBUM = URL_API_DEEZER + "album/"
URL_API_DEEZER_SEARCH = URL_API_DEEZER + "search?q="


class DeezerArtistView(APIView):
    permission_classes = ()

    def get(self, request, id=None):
        print(id)
        response = requests.get(URL_API_DEEZER_ARTIST + str(id))
        return Response(response.json())


class DeezerAlbumView(APIView):
    permission_classes = ()

    def get(self, request, id=None):
        print(id)
        response = requests.get(URL_API_DEEZER_ALBUM + str(id))
        return Response(response.json())


query_param = openapi.Parameter(
    "q", openapi.IN_QUERY, description="string to search", type=openapi.TYPE_STRING
)


class DeezerSongView(APIView):
    permission_classes = ()

    @swagger_auto_schema(
        manual_parameters=[
            query_param,
        ]
    )
    def get(self, request):
        q = request.GET.get("q")
        response = requests.get(URL_API_DEEZER_SEARCH + str(q))
        return Response(response.json())


class UserViewSet(views.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(id=user.id)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=serializers.LogoutSerializer)
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = ()

    @swagger_auto_schema(request_body=serializers.RegisterSerializer)
    def post(self, request):
        # Validating our serializer from the UserRegistrationSerializer
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Everything's valid, so send it to the UserSerializer
        model_serializer = serializers.UserSerializer(data=serializer.data)
        print(serializer.data)
        model_serializer.is_valid(raise_exception=True)
        user = model_serializer.save()
        refresh = RefreshToken.for_user(user)
        response = {
            "user": model_serializer.data,
            "auth": {"refresh": str(refresh), "access": str(refresh.access_token)},
        }

        return Response(response)
