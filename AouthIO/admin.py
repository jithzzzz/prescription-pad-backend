from django.contrib import admin
from .models import ClientUser, BloodType, PatientDetails, medsDeatils, Diagnostics, Docterreferrence, PRBase, \
    prescriptionRecords, PrLabTest, PrDaignosis, PrExistingDaignosis, LabTestRecords
# Register your models here.

admin.site.register(ClientUser)
admin.site.register(BloodType)
admin.site.register(PatientDetails)
admin.site.register(medsDeatils)
admin.site.register(Diagnostics)
admin.site.register(Docterreferrence)
admin.site.register(PRBase)
admin.site.register(prescriptionRecords)
admin.site.register(PrLabTest)
admin.site.register(PrDaignosis)
admin.site.register(PrExistingDaignosis)
admin.site.register(LabTestRecords)