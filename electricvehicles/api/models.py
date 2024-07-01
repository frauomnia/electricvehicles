from django.db import models

class Location(models.Model):
    postalCode = models.IntegerField(primary_key=True, null=False, blank=False)
    state = models.CharField(max_length=256, null=False, blank=False)
    county = models.CharField(max_length=256, null=False, blank=False)
    city = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return "{} {} {} {}".format(self.state, self.city, self.county, self.postalCode)

class VehicleMake(models.Model):
    vehicleMake = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.vehicleMake

class ElectricRange(models.Model):
    electricRange = models.CharField(max_length=256, null=False, blank=False)

    def __int__(self):
        return self.electricRange

class ElectricVehicleType(models.Model):
    vehicleType = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.vehicleType

class VehicleModel(models.Model):
    vehicleModel = models.CharField(max_length=256, null=False, blank=False)
    modelYear = models.IntegerField(null=False, blank=False)
    vehicleMake = models.ForeignKey(VehicleMake, on_delete=models.DO_NOTHING)
    electricRange = models.ForeignKey(ElectricRange, on_delete=models.DO_NOTHING)
    vehicleType = models.ForeignKey(ElectricVehicleType, on_delete=models.DO_NOTHING)
    regLocation = models.ManyToManyField(Location, through="VehicleLocationLink")
    access = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        unique_together = ('vehicleModel', 'modelYear', 'vehicleMake', 'electricRange', 'vehicleType')
    
    def __str__(self):
        return self.vehicleModel 

class VehicleLocationLink(models.Model):
    vehicleModel = models.ForeignKey(VehicleModel, on_delete=models.DO_NOTHING)
    regLocation = models.ForeignKey(Location, on_delete=models.DO_NOTHING)

class EconnectorType(models.Model):
    connectorType = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.connectorType 

class AccessCode(models.Model):
    accessCode = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.accessCode 

class EvChargingStations(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    stationName = models.CharField(max_length=256, null=False, blank=False)
    stationAddress = models.CharField(max_length=256, null=False, blank=False)
    stationPhone = models.CharField(max_length=256, null=True, blank=True)
    connectorType = models.ForeignKey(EconnectorType, on_delete=models.CASCADE)
    accessCode = models.ForeignKey(AccessCode, on_delete=models.CASCADE)
    stationLocation = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.stationName 
