import csv
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    buses = []
    with open(settings.BUS_STATION_CSV, encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            station = {
                'Name': row.get('Name'),
                'Street': row.get('Street'),
                'District': row.get('District')
            }
            buses.append(station)

    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(buses, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
