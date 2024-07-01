import factory 
from random import randint
from random import choice
from django.test import TestCase 
from django.conf import settings
from django.core.files import File

from .models import *

class MakeFactory(factory.django.DjangoModelFactory):
    vehicleMake = factory.Faker('sentence', nb_words=1)

    class Meta:
        model = VehicleMake

class RangeFactory(factory.django.DjangoModelFactory):
    electricRange = randint(10, 300)

    class Meta:
        model = ElectricRange

class TypeFactory(factory.django.DjangoModelFactory):
    vehicleType = choice(['Battery Electric Vehicle (BEV)', 'Plug-in Hybrid Electric Vehicle (PHEV)'])

    class Meta:
        model = ElectricVehicleType

class VehicleFactory(factory.django.DjangoModelFactory):
    vehicleModel = factory.Faker('sentence', nb_words=1)
    modelYear = randint(1000, 3000)
    vehicleMake = factory.SubFactory(MakeFactory)
    electricRange = factory.SubFactory(RangeFactory)
    vehicleType = factory.SubFactory(TypeFactory)

    class Meta: 
        model = VehicleModel

class LocationFactory(factory.django.DjangoModelFactory):
    postalCode = randint(90000, 100000)
    city = factory.Faker('sentence', nb_words=1)
    state = factory.Faker('sentence', nb_words=1)
    county = factory.Faker('sentence', nb_words=1)

    class Meta: 
        model = Location

class ConnectorFactory(factory.django.DjangoModelFactory):
    connectorType = factory.Faker('sentence', nb_words=3)

    class Meta:
        model = EconnectorType

class AccessFactory(factory.django.DjangoModelFactory):
    accessCode = choice(['public', 'private'])

    class Meta:
        model = AccessCode

class StationFactory(factory.django.DjangoModelFactory):
    id = randint(0, 100000)
    stationName = factory.Faker('sentence', nb_words=10)
    stationAddress = factory.Faker('sentence', nb_words=10)
    stationPhone = 888-999-4444
    connectorType = factory.SubFactory(ConnectorFactory)
    accessCode = factory.SubFactory(AccessFactory)
    stationLocation = randint(0, 100000)

    class Meta: 
        model = EvChargingStations