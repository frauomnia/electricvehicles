from django.urls import include, path
from . import views 
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('evehicles/', views.VehicleList.as_view(), name='evehicles'),
    path('evehicle/<int:id>', views.evehicle, name='evehicle'),
    path('locationDetails/<int:postalCode>', views.locationDetails, name='locationDetails'),
    path('modelYear/<int:year>', views.modelYear, name='modelYear'),
    path('make/', views.make, name='make'),
    path('year/', views.year, name='year'),
    path('location/', views.location, name='location'),
    path('makeVehicles/<int:id>', views.makeVehicles, name='makeVehicles'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('chargingStations/', views.chargingStations, name='chargingStations'),
    path('echargingStation/<int:id>', views.echargingStation, name='echargingStation'),
    path('create_vehicleModel/', views.create_vehicleModel, name='create_vehicleModel'),
  
  #API ENDPOINTS
  ##returns all EV details, location where similar EV models are registered and how many of them in specific location
    path('api/vehicle/<int:id>', api.vehicle_detail, name='vehicle_api'),
  ##create a new vehicle, get a random vehicle as example
    path('api/vehicle/', api.vehicle_create, name='vehicle_create_api'),
  ##returns all EV models registered in WA state filtered by their Make 
    #example: api/vehicles/TESLA will return all TESLA models registered in WA state
    path('api/vehicles/<str:vehicleMake>', api.vehicles_filter_make, name='vehicles_make_api'),
  ##returns all EV models of specific Make that are greater than given Electric Range
    path('api/vehicles/<str:vehicleMake>/<int:electricRange>', api.vehicles_filter_range, name='vehicles_make_range_api'),
  ##returns all the vehicles 
    path('api/vehicles', api.vehicles_list, name='vehicles_api'),
  ##returns all vehicles registered in a location 
      path('api/location/<int:location>', api.vehicles_filter_location, name='location_api'),
  ##returns all the ev charging stations 
    path('api/stations/', api.stations, name='stations_api'),
  ##returns all EV charging stations filtered by Location
    path('api/stations/<int:location>', api.stations_filter_location, name='stations_locations_api'),
  ##returns all EV charging stations filtered by Location and connector type
    path('api/stations/<int:location>/<str:connectorType>', api.stations_filter_connector, name='stations_locations_connector_api'),
]