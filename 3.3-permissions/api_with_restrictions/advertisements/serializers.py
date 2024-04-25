from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from advertisements.models import Advertisement, FavouriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context['request'].user.is_staff:
            return data

        open_adv_counter = len(Advertisement.objects.filter(
            creator=self.context['request'].user, status='OPEN')
        )
        if self.context['request'].method == 'POST' \
                and open_adv_counter >= 10\
                and data.get('status') != 'DRAFT':
            raise ValidationError('У вас не может быть более 10 открытых объявлений')
        if self.context['request'].method in ['PATCH', 'PUT'] \
                and data.get('status') == 'OPEN' \
                and open_adv_counter >= 10:
            raise ValidationError('У вас не может быть более 10 открытых объявлений')
        return data

    def validate_status(self, value):
        """Метод для валидации поля 'status'. Вызывается при обновлении."""

        adv_id = self.context['view'].kwargs['pk']
        if self.context['request'].method in ['PATCH', 'PUT']:
            if Advertisement.objects.filter(id=adv_id, status__exact=value):
                raise ValidationError('Объявление уже имеет указанный статус')
        return value

    def to_representation(self, instance):
        """Метод для представления данных."""

        rep = super().to_representation(instance)
        if self.context['request'].user.is_staff:
            return rep
        elif rep.get('status') == 'DRAFT' and rep.get('creator').get('id') != self.context['request'].user.id:
            pass
        else:
            return rep


class FavouriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""

    user = UserSerializer(
        read_only=True,
    )
    advertisement = AdvertisementSerializer(
        read_only=True,
    )

    class Meta:
        model = FavouriteAdvertisement
        fields = ('user', 'advertisement')

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["user"] = self.initial_data['user']
        validated_data["advertisement"] = self.initial_data['advertisement']
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.initial_data['advertisement'].status == 'DRAFT':
            raise PermissionDenied

        if self.initial_data['user'].id == self.initial_data['advertisement'].creator.id:
            raise ValidationError('Вы не можете добавить свое объявление в избранное')

        if FavouriteAdvertisement.objects.filter(
                user_id=self.initial_data['user'].id,
                advertisement_id=self.initial_data['advertisement'].id
        ):
            raise ValidationError('Нельзя добавить объявление в избранное дважды')
        return data

    def to_representation(self, instance):
        """Метод для представления данных."""

        rep = super().to_representation(instance)
        rep.pop('user')
        return rep
