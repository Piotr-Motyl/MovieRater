from django.contrib.auth.models import User
from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer, UserSerializer


class MovieSetPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 10
    page_query_param = "page_size"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "movie_description", "year"]
    search_fields = "__all__"
    ordering_fields = [
        "id",
        "title",
        "year",
    ]
    pagination_class = MovieSetPagination

    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        return Movie.objects.all()

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.title = request.data["title"]
        movie.movie_description = request.data["movie_description"]
        movie.premiere = request.data["premiere"]
        movie.year = request.data["year"]
        movie.save()

        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()
        return Response("Movie has been deleted")

    @action(methods=["POST"], detail=True)
    def premiere_done(self, request, **kwargs):
        # pylint: disable=unused-argument
        movie = self.get_object()
        movie.premiere = True
        movie.save()

        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
