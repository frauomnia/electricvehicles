import json
from django.test import TestCase
from django.urls import reverse
#takes path of URL's file and turns it into URL string
from django.urls import reverse_lazy 

#test rest_framework classes
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

#import all factories and serializers
from .model_factories import * 
from .serializers import * 


class VehicleSerializerTest(APITestCase):
    vehicle = None
    vehicleserializer = None

    def setUp(self):
        self.vehicle = VehicleFactory.create()
        self.vehicleserializer = VehicleSerializer(instance=self.vehicle)

    def tearDown(self):
        VehicleMake.objects.all().delete()
        ElectricVehicleType.objects.all().delete()
        ElectricRange.objects.all().delete()
        VehicleModel.objects.all().delete()
        RangeFactory.reset_sequence(0)
        TypeFactory.reset_sequence(0)
        MakeFactory.reset_sequence(0)

    def test_vehicleSerializer(self):
        data = self.vehicleserializer.data
        self.assertEqual(set(data.keys()), set(['id', 'vehicleModel', 'modelYear', 'vehicleMake', 'electricRange', 'vehicleType']))

    def test_vehicleSerializerModelHasCorrectData(self):
        data = self.vehicleserializer.data
        self.assertEqual(data['vehicleModel'], self.vehicle.vehicleModel)
        self.assertEqual(data['modelYear'], self.vehicle.modelYear)

class VehicleTest(APITestCase):

    location = None
    vehicle = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        self.vehicle = VehicleFactory.create()
        self.location = LocationFactory.create()
        self.delete_url = reverse('vehicle_api', kwargs={'id': self.vehicle.id})

    def tearDown(self):
        VehicleMake.objects.all().delete()
        ElectricVehicleType.objects.all().delete()
        ElectricRange.objects.all().delete()
        VehicleModel.objects.all().delete()
        RangeFactory.reset_sequence(0)
        TypeFactory.reset_sequence(0)
        MakeFactory.reset_sequence(0)

    def test_vehicleDetialReturnSuccess(self): 
        good_url = reverse('vehicle_api', kwargs={'id': self.vehicle.id})
        response = self.client.get(good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('modelYear' in data)
        self.assertTrue('vehicleModel' in data)
        self.assertEqual(data['modelYear'], self.vehicle.modelYear)
        self.assertEqual(data['vehicleModel'], self.vehicle.vehicleModel)

    def test_vehicleDetailReturnFailOnBadId(self):
        bad_url = '/api/vehicle/Friends/'
        response = self.client.get(bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_vehicleDetailDeleteIsSuccessful(self):
        response = self.client.delete(self.delete_url, format='json')
        self.assertEqual(response.status_code, 204)

    def test_vehicleFilterMakeReturnSuccess(self):
        good_url = reverse('vehicles_make_api', kwargs={'vehicleMake': self.vehicle.vehicleMake})
        response = self.client.get(good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)

    def test_vehicleFilterMakeRangeReturnSuccess(self):
        kwargs={'vehicleMake': self.vehicle.vehicleMake, 'electricRange': int(self.vehicle.electricRange)}
        good_url = reverse('vehicles_make_range_api', kwargs=kwargs)
        response = self.client.get(good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)

    def test_vehiclesFilterLocationeReturnSuccess(self):
        good_url = reverse('location_api', kwargs={'location': self.location.postalCode})
        response = self.client.get(good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)


class StationsTest(APITestCase):
    station = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        self.station = StationFactory.create()

    def tearDown(self):
        AccessCode.objects.all().delete()
        EconnectorType.objects.all().delete()
        EvChargingStations.objects.all().delete()

    def test_stationsFilterLocationReturnSuccess(self): 
        good_url = reverse('stations_locations_api', kwargs={'location': self.station.stationLocation})
        response = self.client.get(good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertTrue('stationName' in data[0])
        self.assertTrue('stationAddress' in data[0])

