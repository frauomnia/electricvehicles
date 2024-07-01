from django.contrib import admin
from .models import *

class VehicleLocationLinkInLine(admin.TabularInline):
    model = VehicleLocationLink
    extra = 1

class LocationAdmin(admin.ModelAdmin): 
    list_display = ('postalCode', 'state', 'city', 'county')

class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ('vehicleMake',)

class ElectricRangeAdmin(admin.ModelAdmin):
    list_display = ('electricRange', )

class ElectricVehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('vehicleType', )

class VehicleModelAdmin(admin.ModelAdmin): 
    list_display = ('vehicleModel', 'modelYear')
    inlines = [VehicleLocationLinkInLine]

class EconnectorTypeAdmin(admin.ModelAdmin):
    list_display = ('connectorType', )

class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('accessCode', )

class EvChargingStationsAdmin(admin.ModelAdmin):
    list_display = ('stationName', 'stationAddress', 'stationPhone', )

admin.site.register(Location, LocationAdmin)
admin.site.register(VehicleMake, VehicleMakeAdmin)
admin.site.register(ElectricRange, ElectricRangeAdmin)
admin.site.register(VehicleModel, VehicleModelAdmin)
admin.site.register(ElectricVehicleType, ElectricVehicleTypeAdmin)
admin.site.register(EconnectorType, EconnectorTypeAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(EvChargingStations, EvChargingStationsAdmin)