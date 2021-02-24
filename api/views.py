from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (decorators, filters, generics, mixins, permissions,
                            status, viewsets)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Profile, Review, Title
from .permissions import (IsAdminOrDeny, IsAdminOrReadOnly, IsOwnerOrReadOnly,
                          IsOwnerOrStaffOrReadOnly)
from .serializers import (CategorieSerializer, CommentSerializer,
                          CreateProfileSerializer, CreateTitleSerializer,
                          GenreSerializer, ProfileSerializer,
                          RetrieveTokenSerializer, ReviewSerializer,
                          TitleSerializer)


class BaseListCreateDestroyViewSet(
        viewsets.ViewSet,
        generics.CreateAPIView,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin):
    pass


class CategoriesViewSet(BaseListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)


class GenresViewSet(BaseListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, DjangoFilterBackend, )
    filterset_class = TitleFilter
    filterset_fields = ('name', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly, )

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return CreateTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )

    def get_queryset(self) -> QuerySet:
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer) -> None:
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )

    def get_queryset(self) -> QuerySet:
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer) -> None:
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdminOrDeny, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']

    @decorators.action(
        methods=('GET', 'PATCH'),
        detail=False,
        permission_classes=(IsAuthenticated, IsOwnerOrReadOnly, ),
    )
    def me(self, request) -> Response:
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        role = request.user.role
        serializer = self.get_serializer(
            instance=request.user, data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=role)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@decorators.permission_classes([AllowAny])
@decorators.api_view(['POST'])
def register_user(request):
    serializer = CreateProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user = Profile.objects.get_or_create(email=email, username=username)
    code = default_token_generator.make_token(user[0])
    send_mail('Confirmation code', code,
              getattr(settings, "DEFAULT_FROM_EMAIL"), [email], )
    return Response(data=serializer.data,
                    status=status.HTTP_200_OK)


@decorators.permission_classes([AllowAny])
@decorators.api_view(['POST'])
def retrieve_token(request):
    serializer = RetrieveTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    user = get_object_or_404(Profile, email=data['email'])
    if default_token_generator.check_token(user, data['confirmation_code']):
        token = RefreshToken.for_user(user)
        token = {'token': token.access_token}
        return Response(data=token,
                        status=status.HTTP_200_OK)
    return Response(data={'confirmation_code': 'not valid'},
                    status=status.HTTP_400_BAD_REQUEST)
