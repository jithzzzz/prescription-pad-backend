"""prescriptionpad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from AouthIO import views
# from AouthIO.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=True)),
    path('patient-details', views.patient_list),
    path('bloodtypes', views.bloodtype_list),
    path('meds-details', views.medicinedetails),
    path('dignosticsdetails', views.dignosticsdetails),
    path('PatientHistory/<str:id>', views.PatientHistory),
    path('PatientHistorySearch/<str:key>', views.PatientHistorySearch),
    path('PatientListSearch/<str:key>', views.patient_list_search),
    path('Login', views.AdminLogin),
    path('LogOut', views.AdminLogOut),
    path('new-prescription', views.NewPrescription),
    path('referancedetails', views.referancedetails),
    # path('pdf_view/<str:key>', views.pdf_view),
    path('change-password', views.ChagePassowrd),
    path('pdf_view_new/<str:key>', views.ViewPDF.as_view(), name="pdf_view"),
]
