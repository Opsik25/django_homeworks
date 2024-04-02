from django.http import Http404
from django.shortcuts import render

from main.models import Car, Sale


def cars_list_view(request):
    car_model = request.GET.get('q')
    if car_model is None:
        cars = Car.objects.all()
    else:
        cars = Car.objects.filter(model__icontains=car_model)
    template_name = 'main/list.html'
    return render(request, template_name, {'cars': cars})


def car_details_view(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        template_name = 'main/details.html'
        return render(request, template_name, {'car': car})
    except Car.DoesNotExist:
        raise Http404


def sales_by_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        sales = Sale.objects.filter(car_id=car_id)
        template_name = 'main/sales.html'
        context = {
            'car': car,
            'sales': sales
        }
        return render(request, template_name, context)
    except Car.DoesNotExist:
        raise Http404('Car not found')
