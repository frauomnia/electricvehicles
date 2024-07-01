from django import forms
from django.forms import ModelForm
from .models import *

class VehicleModelForm(ModelForm):
    class Meta:
        model = VehicleModel
        fields = ['vehicleModel', 'modelYear', 'vehicleMake', 'vehicleType', 'electricRange', 'regLocation']

    #data input validation
    def clean(self):
        cleaned_data = super(VehicleModelForm, self).clean()
        modelYear = cleaned_data.get('modelYear')
        if not (len(str(modelYear)) == 4):
            raise forms.ValidationError("Please insert a valid year")
        return(cleaned_data)


            

