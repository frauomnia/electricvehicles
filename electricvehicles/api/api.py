from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import random
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import * 
from .serializers import *

## EVs
@api_view(['GET', 'POST'])
def vehicle_create(request):
    if request.method == 'POST':
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        #get a random vehicle as an example 
        vehicles_test = list(VehicleModel.objects.all().values('id'))
        list_test = [x['id'] for x in vehicles_test]
        vehicle = VehicleModel.objects.get(id=random.choice(list_test))
    except VehicleModel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PUT'])
def vehicle_detail(request, id):
    try:
        vehicle = VehicleModel.objects.get(id=id)
    except VehicleModel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = VehicleSerializer(vehicle)
        #get registeration location for the vehicle model and their count 
        locationLinks = vehicle.vehiclelocationlink_set.all().values('regLocation_id').annotate(Count('regLocation_id')).order_by('-regLocation_id__count')
        vehicleData = serializer.data
        #add the list of registeration locations per vehicle model to the return dict
        vehicleData.update({'Registeration locations': locationLinks})
        return Response(vehicleData)
    elif request.method == 'DELETE':
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def vehicles_list(request):
    try:
        vehicles = VehicleModel.objects.all()
    except VehicleModel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def vehicles_filter_location(request, location):
    try:
        vehicles = VehicleModel.objects.all()
    except VehicleModel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        locations = Location.objects.get(postalCode=location)
        vehiclesLocation = locations.vehiclemodel_set.all()
        countID = {'number of e-vehicles registered in postal code': locations.vehiclemodel_set.all().count()}
        serializer = VehiclesSerializer(vehiclesLocation, many=True)
        vehicleData = serializer.data
        vehicleData.insert(0, dict(countID))
        return Response(vehicleData)

@api_view(['GET'])
def vehicles_filter_make(request, vehicleMake):
    try:
        vehicleMake = VehicleMake.objects.get(vehicleMake=vehicleMake)
        vehicles = VehicleModel.objects.filter(vehicleMake=vehicleMake).filter(vehicleType__vehicleType__icontains='BEV')
    except VehicleModel.DoesNotExist or VehicleMake.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def vehicles_filter_range(request, vehicleMake, electricRange):
    try:
        electricRange = ElectricRange.objects.get(electricRange=electricRange)
        vehicleMake = VehicleMake.objects.get(vehicleMake=vehicleMake)
        vehicles = VehicleModel.objects.filter(vehicleMake=vehicleMake).filter(electricRange=electricRange)
    except VehicleModel.DoesNotExist or ElectricRange.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response(serializer.data)

## EV charging stations
@api_view(['GET'])
def stations(request):
    try:
        stations = EvChargingStations.objects.all()
    except EvChargingStations.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = StationsSerializer(stations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def stations_filter_location(request, location):
    try:
        stations = EvChargingStations.objects.filter(stationLocation = location)
    except EvChargingStations.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = StationsSerializer(stations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def stations_filter_connector(request, location, connectorType):
    try:
        connectorType = EconnectorType.objects.get(connectorType = connectorType)
        stations = EvChargingStations.objects.filter(stationLocation = location).filter(connectorType = connectorType)
    except EvChargingStations.DoesNotExist or EconnectorType.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = StationsSerializer(stations, many=True)
    return Response(serializer.data)
