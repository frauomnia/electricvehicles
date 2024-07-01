from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.db.models import Count
from .models import *
from .forms import *

def index(request):
    vehicles = VehicleModel.objects.all()
    return render(request, 'api/index.html', {'vehicles': vehicles})

class VehicleList(ListView):
    model = VehicleModel
    context_object_name = 'evehicles'
    template_name = 'api/evehicles.html'

def evehicle(request, id):
    evehicle = VehicleModel.objects.get(id=id)
    locationLinks = evehicle.vehiclelocationlink_set.all().values('regLocation_id').annotate(Count('regLocation_id'))
    evehicle.access += 1
    evehicle.save()
    return render(request, 'api/evehicle.html', {'evehicle': evehicle, 'locationLinks': locationLinks})
    
def locationDetails(request, postalCode):
    locationDetails = Location.objects.get(postalCode=postalCode)
    chargingStations = EvChargingStations.objects.filter(stationLocation=postalCode)
    return render(request, 'api/locationDetails.html', {'locationDetails': locationDetails , 'chargingStations': chargingStations})

def location(request):
    locations = Location.objects.all()
    return render(request, 'api/location.html', {'locations': locations})

def modelYear(request, year):
    vehicles = VehicleModel.objects.filter(modelYear=year)
    return render(request, 'api/modelYear.html', {'vehicles': vehicles, 'modelYear': year})

def make(request):
    makes = VehicleMake.objects.all()
    return render(request, 'api/make.html', {'makes': makes})

def year(request):
    years = [
        obj['modelYear'] 
        for obj in 
        VehicleModel.objects.values('modelYear').distinct()
    ]
    return render(request, 'api/year.html', {'years': years})

def delete(request, id):
    try:	
        VehicleModel.objects.filter(id=id).delete()
    except IntegrityError:
        pass

    return HttpResponseRedirect('/')

def create_vehicleModel(request):
    if request.method == "POST":
        form = VehicleModelForm(request.POST)
        if form.is_valid():
            vehicleModel = form.save()
            return HttpResponseRedirect('/evehicles/')
        else:
            return render(request, 'api/create_vehicleModel.html', {'error': 'failed', 'form': form})
    else: 
        master_vehicles = VehicleModel.objects.all()
        form = VehicleModelForm()
    return render(request, 'api/create_vehicleModel.html', {'form': form, 'master_vehicles': master_vehicles})

def makeVehicles(request, id):
    vehicleMake = VehicleMake.objects.get(id=id)
    vehicles = VehicleModel.objects.filter(vehicleMake=vehicleMake)
    return render(request, 'api/makeVehicles.html', {'vehicles': vehicles, 'vehicleMake': make})

def chargingStations(request):
    chargingStations = EvChargingStations.objects.all()
    return render(request, 'api/chargingStations.html', {'chargingStations': chargingStations})

def echargingStation(request, id):
    echargingStation = EvChargingStations.objects.get(id=id)
    return render(request, 'api/echargingStation.html', {'echargingStation': echargingStation})

