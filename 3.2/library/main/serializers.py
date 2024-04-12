from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import Book, Order


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(min_length=1)
    title = serializers.CharField(min_length=1)

    class Meta:
        model = Book
        fields = "__all__"

    def validate_year(self, value):
        if value < 1445:
            raise ValidationError('Невозможно. Первый печатный станок изобрели в 1445 году.')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        orders_count = len(instance.books.all())
        representation['orders_count'] = orders_count
        return representation


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(min_length=1)

    class Meta:
        model = Order
        fields = "__all__"

    def validate_days_count(self, value):
        if value > 30:
            raise ValidationError('Не более 30 дней')
        return value

    def validate_books(self, value):
        if len(value) > 3:
            raise ValidationError('Не более 3-х книг в одном заказе!')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        books_details = instance.books.all()
        representation['books'] = []
        for book in books_details:
            representation['books'].append({
                'author': book.author,
                'title': book.title,
                'year': book.year
            })
        return representation
