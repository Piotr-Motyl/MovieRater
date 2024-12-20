from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer, MovieSerializer, ReviewSerializer
from .models import Movie, Review
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import action

class MovieSetPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 10
    page_query_param = 'page_size'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    #queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'movie_description', 'year']
    search_fields = '__all__'
    ordering_fields = ['id', 'title', 'year'] #TODO: ordering=id - parametr pod jakim wysylamy zapytanie, mozna tez tak: ?ordering=-rok, tytul
    pagination_class = MovieSetPagination

    authentication_classes = (TokenAuthentication, ) #tylko dla filmow
    permission_classes = (DjangoModelPermissions, ) #tylko dla filmow, pozwolenia ustawione w sekcji admin

    def get_queryset(self):
        movies = Movie.objects.all()
        return movies

    # def retrieve(self, request, *args, **kwargs):
    #     # GET - nadpisanie metody wbudowanej + ograniczenia dla tworzenia nowych rekordow
    #     required_fields = ['title', 'description', 'premiere', 'year']
    #     for field in required_fields:
    #         if field not in request.data:
    #             return Response({"error": f"Field '{field}' is missing"}, status=400)
    #
    #
    #     movie = Movie.objects.create(title=request.data['title'],
    #                                  movie_description=request.data['movie_description'],
    #                                  premiere=request.data['premiere'],
    #                                  year=request.data['year']
    #                                  )
    #
    #     serializer = MovieSerializer(movie, many=False)
    #     return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.title = request.data['title']
        movie.movie_description = request.data['movie_description']
        movie.premiere = request.data['premiere']
        movie.year = request.data['year']
        movie.save()

        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()
        return Response("Movie has been deleted")
        
    @action(methods=['POST'], detail=True)
    def premiere_done(self, request, **kwargs):
        movie = self.get_object()
        movie.premiere = True
        movie.save()

        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
