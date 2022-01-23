from rest_framework import serializers
from . import models


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientUser
        fields = ('UserName', 'UserId', 'Email', 'Name', 'PublickTocken')


class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BloodType
        fields = ('BloodTypeId', 'bloodType')


class PatientDetailsSerializer(serializers.ModelSerializer):
    extra_field = serializers.SerializerMethodField()
    OPID_filed = serializers.SerializerMethodField()

    def get_extra_field(self, foo_instance):
        return foo_instance.bloodType.bloodType

    def get_OPID_filed(self, foo_instance):
        return str(foo_instance.firstName)[:2].upper() + str(foo_instance.phoneNumber)[5:] + str(str(foo_instance.dob)
                                                                                                .split('-')[0] +
                                                                                                str(foo_instance.dob)
                                                                                                .split('-')[1] +
                                                                                                str(foo_instance.dob).
                                                                                                split('-')[2])


    class Meta:
        model = models.PatientDetails
        fields = ('firstName', 'lastName', 'gender', 'dob',
        'heigth', 'weigth', 'bloodType', 'phoneNumber', 'emailAddress', 'extra_field', 'Update', 'Createdate', 'OPID_filed', 'patient_id')


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.medsDeatils
        fields = ('MId', 'MName', 'MAB', 'MComapnyName', 'Update', 'Createdate', 'Remarks')


class DignoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Diagnostics
        fields = ('DId', 'DName', 'DAB', 'DCty', 'Desicription')

class RefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Docterreferrence
        fields = ('RFId', 'Name', 'Pho', 'Department')

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PRBase
        fields = ('Update', 'patient_id')


