from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter(label='Диапазон дат создания объявления')
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices, lookup_expr='exact', label='Статус объявления')
    creator = filters.NumberFilter(lookup_expr='exact', label='id создателя объявления')
    order_by = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('status', 'status'),
            ('creator', 'creator'),
        )
    )

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
