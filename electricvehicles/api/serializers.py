from rest_framework import serializers
from .models import *

#e-vehicles serializers
class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMake
        fields = ['id', 'vehicleMake']

class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricRange
        fields = ['id', 'electricRange']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricVehicleType
        fields = ['id', 'vehicleType']

class VehicleSerializer(serializers.ModelSerializer):
    vehicleMake = MakeSerializer()
    electricRange = RangeSerializer()
    vehicleType = TypeSerializer()
    class Meta:
        model = VehicleModel
        fields = ['id', 
                    'vehicleModel', 
                    'modelYear', 
                    'vehicleMake', 
                    'electricRange', 
                    'vehicleType']

    def create(self, validated_data):
        make_data = self.initial_data.get('vehicleMake')
        range_data = self.initial_data.get('electricRange')
        type_data = self.initial_data.get('vehicleType')
        vehicle = VehicleModel(**{**validated_data,
                                'vehicleMake': VehicleMake.objects.get(id=make_data['id']),
                                'electricRange': ElectricRange.objects.get(id=range_data['id']),
                                'vehicleType': ElectricVehicleType.objects.get(id=type_data['id']),
                                })
        vehicle.save()
        return vehicle
        
class VehiclesSerializer(serializers.ModelSerializer):
    vehicleMake = MakeSerializer()
    electricRange = RangeSerializer()
    vehicleType = TypeSerializer()
    class Meta:
        model = VehicleModel
        fields = ['id', 
                    'vehicleModel', 
                    'modelYear', 
                    'vehicleMake', 
                    'electricRange', 
                    'vehicleType']

#EV charging stations serializers

class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconnectorType
        fields = ['id', 'connectorType']

class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessCode
        fields = ['id', 'accessCode']

class StationsSerializer(serializers.ModelSerializer):
    connectorType = ConnectorSerializer()
    accessCode = AccessSerializer()
    class Meta:
        model = EvChargingStations
        fields = ['id', 
                    'stationName', 
                    'stationAddress', 
                    'stationPhone', 
                    'connectorType', 
                    'accessCode',
                    'stationLocation']
