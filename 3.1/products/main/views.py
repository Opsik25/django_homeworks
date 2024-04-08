from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Product, Review
from main.serializers import ReviewSerializer, ProductListSerializer, ProductDetailsSerializer


@api_view(['GET'])
def products_list_view(request):
    products = Product.objects.all()
    ser = ProductListSerializer(products, many=True)
    return Response(ser.data)


class ProductDetailsView(APIView):
    def get(self, request, product_id):
        product_review = Product.objects.filter(id=product_id)
        if not product_review:
            raise Http404
        else:
            ser = ProductDetailsSerializer(product_review, many=True)
            return Response(ser.data)


# доп задание:
class ProductFilteredReviews(APIView):
    def get(self, request, product_id):
        mark = request.query_params.get('mark')
        if not mark:
            review = Review.objects.filter(product_id=product_id)
        else:
            review = Review.objects.filter(mark=mark, product_id=product_id)
        ser = ReviewSerializer(review, many=True)
        if not ser.data:
            raise Http404
        return Response(ser.data)
