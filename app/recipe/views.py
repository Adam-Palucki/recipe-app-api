from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    '''Manage tags in the database'''
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):  # overriding function
        '''Return object for the current authenticated user only'''
        return self.queryset.filter(user = self.request.user).order_by('-name')

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    '''Manage ingredients in database'''
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):  # overriding function
        '''Return object for the current authenticated user only'''
        return self.queryset.filter(user = self.request.user).order_by('-name')