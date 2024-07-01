import os 
import sys 
import django
import csv
from collections import defaultdict

sys.path.append('../electricvehicles')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electricvehicles.settings')
django.setup()

from api.models import * 
from django.db import IntegrityError
from dataclasses import dataclass

data_evs_Locations = './electric-vehicles-subset.csv'
data_chargingStations = './ev-charging-stations.csv'

#data file: Electric Vehicles and Locations
vehicleMake_set = set()
electricRange_set = set()
vehicleType_set = set()
vehicleModels = set()
modelLocations = defaultdict(list)

#delete all data inserted to start clean
VehicleLocationLink.objects.all().delete()
VehicleModel.objects.all().delete()
VehicleMake.objects.all().delete()
ElectricRange.objects.all().delete()
ElectricVehicleType.objects.all().delete()
Location.objects.all().delete()

#fix error of unhashable object
@dataclass(unsafe_hash=True)
class InMemoryVehicleModel:
    model: str
    year: int
    make: str
    range: int
    car_type: str

with open(data_evs_Locations) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # skip first row
    header = csv_reader.__next__()
    for row in csv_reader:
        location = None
        try:
            location = Location.objects.create(postalCode = row[4], county = row[1], city = row[2], state = row[3])
            location.save()
            # skip IntegrityError due to duplicate values in CSV
        except IntegrityError:
            location = Location(postalCode = row[4], county = row[1], city = row[2], state = row[3])

        vehicleMake_set.add(row[6])
        electricRange_set.add(row[10])
        vehicleType_set.add(row[8])
        
        model = InMemoryVehicleModel(model=row[7], year=row[5], make=row[6], range=row[10], car_type=row[8])
        
        vehicleModels.add(model)
        modelLocations[model].append(location)

vehicleMake_rows = {}
electricRange_rows = {}
vehicleType_rows = {}
vehicleModels_rows = {}


for entry in vehicleMake_set:
    row = VehicleMake.objects.create(vehicleMake=entry)
    row.save()
    vehicleMake_rows[entry] = row

for entry in electricRange_set:
    row = ElectricRange.objects.create(electricRange=entry)
    row.save()
    electricRange_rows[entry] = row

for entry in vehicleType_set:
    row = ElectricVehicleType.objects.create(vehicleType=entry)
    row.save()
    vehicleType_rows[entry] = row

for data in vehicleModels:
    row = VehicleModel.objects.create(
        vehicleModel=data.model, 
        modelYear=data.year, 
        electricRange = electricRange_rows[data.range], 
        vehicleMake = vehicleMake_rows[data.make],
        vehicleType = vehicleType_rows[data.car_type],
    )
    row.save()
    vehicleModels_rows[data] = row

    for location in modelLocations[data]:
        VehicleLocationLink.objects.create(vehicleModel=row, regLocation=location)


#data file: EV Charging Stations

chargingStations = defaultdict(list)
connectorType_set = set()
accessCode_set = set()

with open(data_chargingStations) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # skip first row
    header = csv_reader.__next__()
    for row in csv_reader:

        connectorType_set.add(row[10])
        accessCode_set.add(row[11])
        chargingStations[row[8]] = row[1:3] + row[5:7] + row[10:12]

#delete all data inserted to start clean
EconnectorType.objects.all().delete()
AccessCode.objects.all().delete()
EvChargingStations.objects.all().delete()

connectorType_rows = {}
accessCode_rows = {}

for entry in connectorType_set:
    row = EconnectorType.objects.create(connectorType=entry)
    row.save()
    connectorType_rows[entry] = row

for entry in accessCode_set:
    row = AccessCode.objects.create(accessCode=entry)
    row.save()
    accessCode_rows[entry] = row

for data in chargingStations.items():
    row = EvChargingStations.objects.create(id=data[0], stationName=data[1][0], stationAddress=data[1][1], stationLocation=data[1][2], stationPhone=data[1][3], connectorType=connectorType_rows[data[1][4]], accessCode=accessCode_rows[data[1][5]])
    row.save()



