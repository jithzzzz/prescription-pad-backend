from django.db import models
import uuid
from django.utils import timezone
from django.utils import timezone
from datetime import datetime

# Create your models here.


class ClientUser(models.Model):
    UserId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Email = models.EmailField(default="admin@info.com")
    Name = models.CharField(max_length=30, default="Name")
    UserName = models.CharField(max_length=12, default="User Name")
    Password = models.CharField(max_length=12, default="password")
    Address = models.TextField()
    PublickTocken = models.CharField(max_length=100, default="password")
    PriventTocken = models.CharField(max_length=100, default="password")
    Update = models.DateTimeField(default=timezone.now, blank=True)
    Createdate = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "ClientUsers"

    def __str__(self):
        return self.UserName

    def __int__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("ClientUser_detail", kwargs={"pk": self.pk})


class BloodType(models.Model):
    BloodTypeId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bloodType = models.CharField(max_length=30, default="Name")
    cdate = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "BloodType"

    def __str__(self):
        return self.bloodType


class PatientDetails(models.Model):
    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=100, default="First Name")
    lastName = models.CharField(max_length=100, default="Last Name", blank=True)
    gender = models.CharField(max_length=30, default="Not intrested to share")
    dob = models.DateField(default=timezone.now)
    heigth = models.BigIntegerField(default=00.0, blank=True)
    weigth = models.BigIntegerField(default=00.0, blank=True)
    bloodType = models.ForeignKey(BloodType, on_delete=models.DO_NOTHING)
    phoneNumber = models.BigIntegerField(default=9999999999)
    emailAddress = models.EmailField(default='user@prescriptionpad.in')
    Update = models.DateTimeField(default=timezone.now, blank=True)
    Createdate = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "PatientDetails"

    def __str__(self):
        return str(self.patient_id)


class medsDeatils(models.Model):
    MId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    MName = models.CharField(max_length=500, default="")
    MAB = models.CharField(max_length=500, default="")
    MComapnyName = models.CharField(max_length=500, default="")
    Update = models.DateTimeField(default=timezone.now, blank=True)
    Createdate = models.DateTimeField(default=timezone.now, blank=True)
    Remarks = models.TextField()

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "medsDetails"

    def __str__(self):
        return self.MName


class Diagnostics(models.Model):
    DId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DName = models.CharField(max_length=500, default="")
    DCty = models.CharField(max_length=500, default="")
    DAB = models.CharField(max_length=500, default="")
    Desicription = models.TextField()

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "dignostics"

    def __str__(self):
        return self.DName


class Docterreferrence(models.Model):
    RFId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=500, default="")
    # Address = models.TextField(blank=True)
    Pho = models.BigIntegerField()
    # Email = models.EmailField()
    Department = models.CharField(max_length=500, default="", blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "refdetails"

    def __str__(self):
        return str(self.RFId)


class PRBase(models.Model):
    Bid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.ForeignKey(PatientDetails, on_delete=models.DO_NOTHING)
    Update = models.DateTimeField(default=timezone.now, blank=True)
    Createdate = models.DateTimeField(default=timezone.now, blank=True)
    RFId = models.CharField(max_length=1000, default="", blank=True)
    medical_condition = models.TextField(blank=True)
    refnote = models.TextField(blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "PRBase"

    def __str__(self):
        return str(self.Bid)


class prescriptionRecords(models.Model):
    PRId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Bid = models.ForeignKey(PRBase, on_delete=models.DO_NOTHING)
    medicin = models.ForeignKey(medsDeatils, on_delete=models.DO_NOTHING)
    time = models.CharField(max_length=500, default="")
    days = models.BigIntegerField()
    remarks = models.TextField(blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "prescriptionRecords"


class PrLabTest(models.Model):
    PRLABID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Bid = models.ForeignKey(PRBase, on_delete=models.DO_NOTHING)
    labtest = models.CharField(max_length=500, default="")

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "PrLabTest"


class PrDaignosis(models.Model):
    PRDIGID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Bid = models.ForeignKey(PRBase, on_delete=models.DO_NOTHING)
    DId = models.ForeignKey(Diagnostics, on_delete=models.DO_NOTHING)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "PrDaignosis"

class PrExistingDaignosis(models.Model):
    PREXDIGID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Bid = models.ForeignKey(PRBase, on_delete=models.DO_NOTHING)
    diagnosis = models.TextField(blank=True)

    class Meta:
        # verbose_name = _("ClientUser")
        verbose_name_plural = "PrExistingDaignosis"


class LabTestRecords(models.Model):
    Bid = models.ForeignKey(PRBase, on_delete=models.DO_NOTHING)
    LabRecordId =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    LabTestName = models.CharField(max_length=1000, blank=True, default='')
    LabTestDate = models.DateField(default=timezone.now, blank=True)
    LabTestResult = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "LabTestRecords"

