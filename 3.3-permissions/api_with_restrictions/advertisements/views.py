from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavouriteAdvertisement
from advertisements.permissions import IsOwner, IsDraftRetrieve
from advertisements.serializers import AdvertisementSerializer, FavouriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["destroy", "update", "partial_update"]:
            return [IsOwner()]
        if self.action == "retrieve":
            return [IsDraftRetrieve()]
        return []

    @action(detail=True, methods=['POST'])
    def add_favourite(self, request, pk=None):
        advertisement = self.get_object()
        user = request.user
        data = {
            'user': user,
            'advertisement': advertisement,
        }
        serializer = FavouriteAdvertisementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def favourites(self, request):
        my_favourites = FavouriteAdvertisement.objects.filter(user_id=request.user.id)
        serializer = FavouriteAdvertisementSerializer(my_favourites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'])
    def del_favourite(self, request, pk=None):
        advertisement_id = self.get_object().id
        user_id = request.user.id
        fav_adv = FavouriteAdvertisement.objects.filter(advertisement_id=advertisement_id, user_id=user_id)
        if fav_adv:
            fav_adv.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Объявление отсутствует в избранных', status=status.HTTP_400_BAD_REQUEST)
