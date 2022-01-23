from pyexpat import model
from django.shortcuts import render
from rest_framework import viewsets
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Sum

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from textwrap import wrap

from django.http import FileResponse
import io

from . import models
from . import serializers

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from datetime import date, timedelta

from uuid import uuid4


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF


class ViewPDF(View):
    def get(self, request, key, *args, **kwargs):
        print(key)
        name, opid, gender, age, prescriptionDetails, medical_dis, refnote, labtest = pdf_view(key)
        final_lab_test_string = ''
        for i in range(len(labtest)):
            if(i == len(labtest)-1):
                final_lab_test_string = labtest[i]['labtest']
            else:
                final_lab_test_string = labtest[i]['labtest'] + ', '
        print(final_lab_test_string)
        pp = []
        for i in prescriptionDetails:
            meds = models.medsDeatils.objects.get(MId=i['medicin_id'])
            if(len(i['remarks'].split('@')) == 2):
                k = i['remarks'].split('@')[0]
                y = i['remarks'].split('@')[1]
            else:
                k = i['remarks']
                y = ''
            md = meds.MName
            m = [md, i['time'], 'X ' + str(i['days']) + ' days']
            pp.append(m)
        
        print(pp, "YYYYYYYY")
        if(gender == 'male'):
            gender = 'M'
        else:
            gender = 'F'

        data = {
            "date": date.today(),
            "patient_id": opid,
            'bio': name + ', ' + str(age) + ' years, ' + gender,
            'data': pp,
            'medical_dis': medical_dis,
            'refnote': refnote,
            'final_lab_test_string': final_lab_test_string
        }

        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')




# Admin Login
@api_view(['POST'])
def AdminLogin(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        UserName = user_data['UserName']
        Password = user_data['Password']
        if models.ClientUser.objects.filter(Q(UserName=UserName) & Q(Password=Password)):
            rand_token = uuid4()
            models.ClientUser.objects.filter(Q(UserName=UserName) & Q(Password=Password)).update(PublickTocken=rand_token)
            user = models.ClientUser.objects.filter(
                Q(UserName=UserName) & Q(Password=Password))
            user_serializer = serializers.LoginSerializer(user, many=True)
            return JsonResponse(user_serializer.data, safe=False)
        else:
            return JsonResponse({'Message': 'No user found'}, status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['POST'])
def AdminLogOut(request):
    if(request.method == 'POST'):
        user_data = JSONParser().parse(request)
        UserName = user_data['UserName']
        if models.ClientUser.objects.filter(UserName=UserName):
             models.ClientUser.objects.filter(UserName=UserName).update(PublickTocken='')
             return JsonResponse({'Message':'Successfully logged out'})
        else:
            return JsonResponse({'Message': 'User not found'})
    else:
        return JsonResponse({'Message': 'Invalid method'})



@api_view(['POST'])
def ChagePassowrd(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        Email = user_data['email']
        exPassword = user_data['expassword']
        newPassword = user_data['Newpassword']
        if models.ClientUser.objects.filter(Q(Email=Email) & Q(Password=exPassword)):
            models.ClientUser.objects.filter(
                Email=Email).update(Password=newPassword)
            return JsonResponse({'Message': 'Password Changed!!'})
        else:
            return JsonResponse({'Message': 'No user found'}, status=status.HTTP_204_NO_CONTENT, safe=False)
    else:
        return JsonResponse({'Message': 'Method not allowd'})


# Patient Details oprations
@api_view(['GET', 'POST', 'DELETE'])
def patient_list(request):
    if request.method == 'GET':
        patients = models.PatientDetails.objects.all()
        if len(list(patients)) > 0:
            patient_serializer = serializers.PatientDetailsSerializer(
                patients, many=True)
            return JsonResponse(patient_serializer.data, safe=False)
        else:
            return JsonResponse({'Data': 'No Records Available'}, status=status.HTTP_204_NO_CONTENT, safe=False)
    elif request.method == 'POST':
        try:
            patient_data = JSONParser().parse(request)
            print(patient_data)
            bdata = models.BloodType.objects.get(
                BloodTypeId=patient_data['bloodType'])
            patient_data['bloodType'] = bdata.BloodTypeId
            print(patient_data)
            patient_serializer = serializers.PatientDetailsSerializer(
                data=patient_data)
            print("**********************")
            if patient_serializer.is_valid():
                print("&&&&&&&&&&&&&&&&&7")
                patient_serializer.save()
                return JsonResponse(patient_serializer.data, status=status.HTTP_201_CREATED, safe=False)
            else:
                return JsonResponse(patient_serializer, safe=False)
        except Exception as e:
            return JsonResponse({"Error": str(e)})
            print(e)


@api_view(['GET', 'POST', 'DELETE'])
def patient_list_search(request, key):
    if request.method == 'POST':
        try:
            id = ''
            finalgenaratedid = []
            if key.isnumeric():
                data = models.PatientDetails.objects.get(phoneNumber=int(key))
                id = data.patient_id
            elif key.isalpha():
                data = models.PatientDetails.objects.get(firstName=key)
                id = data.patient_id
            else:
                data = models.PatientDetails.objects.all().values()
                for i in data:
                    opi = str(i['firstName'])[:2].upper() + str(i['phoneNumber'])[5:] + str(str(i['dob']).split('-')[0] +
                                                                                            str(i['dob']).split('-')[1] +
                                                                                            str(i['dob']).split('-')[2])
                    if opi == key.upper():
                        id = i['patient_id']
            patients = models.PatientDetails.objects.filter(
                patient_id=id).values()

            if len(list(patients)) > 0:
                for i in patients:
                    opi = str(i['firstName'])[:2].upper() + str(i['phoneNumber'])[5:] + str(str(i['dob']).split('-')[0] +
                                                                                            str(i['dob']).split('-')[1] +
                                                                                            str(i['dob']).split('-')[2])
                    bData = models.BloodType.objects.get(
                        BloodTypeId=i['bloodType_id'])
                    print("*********************************************************")
                    print(bData.bloodType)
                    print("*********************************************************")
                    tmpdata = {
                        "firstName": i['firstName'],
                        "lastName": i['lastName'],
                        "gender": i['gender'],
                        "dob": i['dob'],
                        "heigth": i['heigth'],
                        "weigth": i['weigth'],
                        "bloodType": i['bloodType_id'],
                        "phoneNumber": i['phoneNumber'],
                        "emailAddress": i['emailAddress'],
                        "Update": i['Update'],
                        "Createdate": i['Createdate'],
                        "OPID_filed": opi,
                        "extra_field": bData.bloodType,
                        "patient_id": i['patient_id']
                    }
                    finalgenaratedid.append(tmpdata)
                return JsonResponse({'Data': finalgenaratedid})
            else:
                return JsonResponse({'Data': 'No Records Available'}, status=status.HTTP_204_NO_CONTENT, safe=False)

        except Exception as e:
            return JsonResponse({'Error': str(e)})
    else:
        return JsonResponse({"Error": 'Invalid Method'})


# Genaral Blood type
@api_view(['GET'])
def bloodtype_list(request):
    if request.method == 'GET':
        bloodtype = models.BloodType.objects.all()
        bloodtype_serializer = serializers.BloodTypeSerializer(
            bloodtype, many=True)
        return JsonResponse(bloodtype_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def medicinedetails(request):
    if request.method == 'GET':
        meds = models.medsDeatils.objects.all()
        meds_serializer = serializers.MedicineSerializer(meds, many=True)
        return JsonResponse(meds_serializer.data, safe=False)
    elif request.method == 'POST':
        meds_data = JSONParser().parse(request)
        print(meds_data)
        meds_serializer = serializers.MedicineSerializer(data=meds_data)
        if meds_serializer.is_valid():
            meds_serializer.save()
            return JsonResponse(meds_serializer.data, status=status.HTTP_201_CREATED, safe=False)
        else:
            print("%%%%%%%%%%%")
            print(meds_serializer.errors)
            return JsonResponse(meds_serializer, safe=False)


@api_view(['GET', 'POST'])
def dignosticsdetails(request):
    if request.method == 'GET':
        digs = models.Diagnostics.objects.all()
        digs_serializer = serializers.DignoSerializer(digs, many=True)
        return JsonResponse(digs_serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        digs_data = JSONParser().parse(request)
        print(digs_data)
        digs_serializer = serializers.DignoSerializer(data=digs_data)
        if digs_serializer.is_valid():
            digs_serializer.save()
            return JsonResponse(digs_serializer.data, status=status.HTTP_201_CREATED, safe=False)
        else:
            print("%%%%%%%%%%%")
            print(digs_serializer.errors)
            return JsonResponse(digs_serializer, safe=False)


@api_view(['GET', 'POST'])
def referancedetails(request):
    if request.method == 'GET':
        ref = models.Docterreferrence.objects.all()
        ref_serializer = serializers.RefSerializer(ref, many=True)
        return JsonResponse(ref_serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        digs_data = JSONParser().parse(request)
        print(digs_data)
        ref_serializer = serializers.RefSerializer(data=digs_data)
        if ref_serializer.is_valid():
            ref_serializer.save()
            return JsonResponse(ref_serializer.data, status=status.HTTP_201_CREATED, safe=False)
        else:
            print("%%%%%%%%%%%")
            print(ref_serializer.errors)
            return JsonResponse(ref_serializer, safe=False)


@api_view(['GET', 'POST'])
def PatientHistory(request, id):
    try:
        if request.method == 'POST':
            pbase = models.PRBase.objects.filter(patient_id=id).values()
            potherdetails = models.PatientDetails.objects.filter(
                patient_id=id).values()
            

            if len(list(potherdetails)) == 1:
                extr_field = models.BloodType.objects.get(
                    BloodTypeId=potherdetails[0]['bloodType_id'])
                print(potherdetails[0]['bloodType_id'])
                opid = str(potherdetails[0]['firstName'])[:2].upper() + str(potherdetails[0]['phoneNumber'])[5:] + \
                    str(str(potherdetails[0]['dob']).split('-')[0] + str(potherdetails[0]['dob']).split('-')[1] +
                        str(potherdetails[0]['dob']).split('-')[2])
                dignosis_tmp = ''
                labtest_tmp = []
                prescrip_record = []
                labdummy = []
                finalData = []
                print(potherdetails, " #######")
                if len(list(pbase)) > 0:
                    for item in pbase:
                        print('Ok', item['Bid'])
                        dignosis = models.PrDaignosis.objects.filter(
                            Bid=item['Bid']).values('DId')
                        for i in dignosis:
                            # print(i['DId'])
                            k = models.Diagnostics.objects.get(DId=i['DId'])
                            dignosis_tmp = dignosis_tmp + k.DName + ', '

                        labtest = models.PrLabTest.objects.filter(
                            Bid=item['Bid']).values('PRLABID')
                        for i in labtest:
                            # print(i['PRLABID'])
                            k = models.PrLabTest.objects.get(
                                PRLABID=i['PRLABID'])

                            labtest_tmp.append(k.labtest)
                            # print('kp ********************* :', k)

                        prreords = models.prescriptionRecords.objects.filter(
                            Bid=item['Bid']).values('PRId')
                        print(len(list(prreords)))
                        for i in prreords:
                            # print(i['PRId'])
                            k = models.prescriptionRecords.objects.filter(
                                PRId=i['PRId']).values()
                            print(k[0]['medicin_id'])
                            p = models.medsDeatils.objects.get(
                                MId=k[0]['medicin_id'])
                            prescrip_record.append(
                                {'prescription': list(k), 'medicine_name': p.MName})
                            print('\n\n')
                            # print(prescrip_record)

                        labdummy = models.LabTestRecords.objects.filter(Bid=item['Bid']).values('LabRecordId', 'LabTestName',
                                                                                                'LabTestDate', 'LabTestResult')

                        finalData.append({'basicData': item, 'patientInfo': list(potherdetails), 'OPID': opid,
                        'dignosis': dignosis_tmp, 'extr_field': extr_field.bloodType, 'labtest': list(labtest_tmp),
                        'prescription_records': list(prescrip_record), 'labTestdata': list(labdummy)})
                else:
                    finalData.append({'patientInfo': list(potherdetails), 'OPID': opid,
                                          'dignosis': dignosis_tmp, 'extr_field': extr_field.bloodType, 'labtest': list(labtest_tmp),
                                          'prescription_records': list(prescrip_record), 'labTestdata': list(labdummy)})

                return JsonResponse(finalData, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse({"Error": 'Patient details not found'})
        else:
            return JsonResponse({"Error": 'Method Not Allowd'})
    except Exception as e:
        print(e)
        return JsonResponse({"Error": str(e)})


@api_view(['POST'])
def NewPrescription(request):
    try:
        if request.method == "POST":
            data = JSONParser().parse(request)
            patient_id = data["patient_id"]
            medical_condition = data["medical_condition"]
            RFId = data["RFId"]
            refnote = data["refnote"]

            priscription_data = data['PRP']
            lab_dat = data['PRLAB']
            dignosis_data = data['PRDIG']

            ex_diagnosis = data["diagnosis"]

            labTestResuts = data["PRLABTest"]

            if models.PatientDetails.objects.get(patient_id=patient_id):
                patient = models.PatientDetails.objects.get(
                    patient_id=patient_id)
                # patient = list(patient)
                prbase = models.PRBase.objects.create(patient_id=patient, RFId=RFId,
                                                      medical_condition=medical_condition, refnote=refnote)
                for i in priscription_data:
                    md = models.medsDeatils.objects.get(MId=i['medicin'])
                    models.prescriptionRecords.objects.create(Bid=prbase, medicin=md, time=i['time'],
                                                              days=i['days'], remarks=i['remarks'])
                for i in lab_dat:
                    models.PrLabTest.objects.create(
                        Bid=prbase, labtest=i['labtest'])

                for i in dignosis_data:
                    dig = models.Diagnostics.objects.get(DId=i['did'])
                    models.PrDaignosis.objects.create(Bid=prbase, DId=dig)

                for i in labTestResuts:
                    models.LabTestRecords.objects.create(
                        Bid=prbase, LabTestName=i['labtest'], LabTestDate=i['date'], LabTestResult=i['result'])

                if(str(ex_diagnosis) != '' or str(ex_diagnosis).upper() != 'NULL'):
                    models.PrExistingDaignosis.objects.create(
                        Bid=prbase, diagnosis=str(ex_diagnosis))

                return JsonResponse({"Message": 'Prescription Created Successfully !!', 'status': True,
                                     'id': str(prbase)})
            else:
                return JsonResponse({"Message": 'No Patient Found !!! Please Create Patient', 'status': False})

            print(data['PRP'][0])
            return JsonResponse({'Data': data})
        else:
            return JsonResponse({"Message": 'Invalid Method !!!', 'status': False})
    except Exception as e:
        return JsonResponse({'Error': str(e), 'status': False})


@api_view(['GET', 'POST'])
def PatientHistorySearch(request, key):
    try:
        if request.method == 'POST':
            id = ''
            if key.isnumeric():
                data = models.PatientDetails.objects.get(phoneNumber=int(key))
                id = data.patient_id
            elif key.isalpha():
                data = models.PatientDetails.objects.get(firstName=key)
                id = data.patient_id
            else:
                data = models.PatientDetails.objects.all().values()
                print("%%%%%%%%%%%%%%%%%")
                for i in data:
                    # print(i)
                    # print("&&&&")
                    opi = str(i['firstName'])[:2].upper() + str(i['phoneNumber'])[5:] + str(str(i['dob']).split('-')[0] +
                                                                                            str(i['dob']).split('-')[1] +
                                                                                            str(i['dob']).split('-')[2])
                    # print(opi, 'opi')
                    if opi == key.upper():
                        id = i['patient_id']
                        print(True)
        # print(id, 'final id')
        pbase = models.PRBase.objects.filter(patient_id=id).values()
        potherdetails = models.PatientDetails.objects.filter(
            patient_id=id).values()
        if len(list(potherdetails)) == 1:
            extr_field = models.BloodType.objects.get(
                BloodTypeId=potherdetails[0]['bloodType_id'])
            print(potherdetails[0]['bloodType_id'])
            opid = str(potherdetails[0]['firstName'])[:2].upper() + str(potherdetails[0]['phoneNumber'])[5:] + \
                str(str(potherdetails[0]['dob']).split('-')[0] + str(potherdetails[0]['dob']).split('-')[1] +
                    str(potherdetails[0]['dob']).split('-')[2])
        dignosis_tmp = ''
        labtest_tmp = []
        prescrip_record = []
        if len(list(pbase)) > 0:
            dignosis = models.PrDaignosis.objects.filter(
                Bid=pbase[0]['Bid']).values('DId')
            for i in dignosis:
                print(i['DId'])
                k = models.Diagnostics.objects.get(DId=i['DId'])
                dignosis_tmp = dignosis_tmp + k.DName + ', '

            labtest = models.PrLabTest.objects.filter(
                Bid=pbase[0]['Bid']).values('PRLABID')
            for i in labtest:
                # print(i['PRLABID'])
                k = models.PrLabTest.objects.get(PRLABID=i['PRLABID'])

                labtest_tmp.append(k.labtest)
                # print('kp ********************* :', k)

            prreords = models.prescriptionRecords.objects.filter(
                Bid=pbase[0]['Bid']).values('PRId')
            print(len(list(prreords)))
            for i in prreords:
                # print(i['PRId'])
                k = models.prescriptionRecords.objects.filter(
                    PRId=i['PRId']).values()
                print(k[0]['medicin_id'])
                p = models.medsDeatils.objects.get(MId=k[0]['medicin_id'])
                prescrip_record.append(
                    {'prescription': list(k), 'medicine_name': p.MName})
                print('\n\n')
                # print(prescrip_record)

        return JsonResponse({'basicData': list(pbase), 'patientInfo': list(potherdetails), 'OPID': opid,
                             'dignosis': dignosis_tmp, 'extr_field': extr_field.bloodType,
                             'labtest': list(labtest_tmp), 'prescription_records': list(prescrip_record)},
                            status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        print(e)
        if str(e) == 'PatientDetails matching query does not exist.':
            return JsonResponse({"Error": 'No records finds related to search'})
        else:
            return JsonResponse({"Error": str(e)})


# @api_view(['GET'])
def pdf_view(key):
    try:
        basicdata = models.PRBase.objects.filter(Bid=key).values()
        basicdata = list(basicdata)
        refnote = basicdata[0]['refnote']
        # red_doc = basicdata[0]['RFId']
        if(models.Docterreferrence.objects.get(RFId=basicdata[0]['RFId'])):
            red_doc = models.Docterreferrence.objects.get(
                RFId=basicdata[0]['RFId'])
            ref_name = red_doc.Name
            ref_dep = red_doc.Department
            ref_pho = red_doc.Pho
        else:
            ref_name = ''
            ref_dep = ''
            ref_pho = ''

        medical_condition = models.PrDaignosis.objects.filter(
            Bid_id=key).values()
        labtest = models.PrLabTest.objects.filter(Bid_id=key).values()
        print(list(labtest), "############")

        # medical_condition = medical_condition.split(',')
        patientdata = models.PatientDetails.objects.get(
            patient_id=basicdata[0]['patient_id_id'])
        name = patientdata.firstName + ' ' + patientdata.lastName
        pho = patientdata.phoneNumber
        gender = patientdata.gender
        today = date.today()
        byear = patientdata.dob.year
        bmonth = patientdata.dob.month
        bdate = patientdata.dob.day
        age = today.year - byear - ((today.month, today.day) < (bmonth, bdate))
        opid = str(patientdata.firstName)[:2].upper() + str(patientdata.phoneNumber)[5:] + \
            str(str(patientdata.dob).split('-')[0] + str(patientdata.dob).split('-')[1] +
                str(patientdata.dob).split('-')[2])


        prescriptionDetails = models.prescriptionRecords.objects.filter(
            Bid=key).values()
        medical_dis = basicdata[0]['medical_condition']
        refnote = basicdata[0]['refnote']

        return(name, opid, gender, age, prescriptionDetails, medical_dis, refnote, list(labtest))
    except Exception as e:
        print(e)
        return JsonResponse({"Error": str(e)})
