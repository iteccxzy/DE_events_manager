import django_filters
from django_filters import CharFilter, DateFilter
from .models import Tutorias, Docentes

from django import forms

class TutoFilter(django_filters.FilterSet):
    fecha= DateFilter(widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}))
    class Meta:
        model= Tutorias
        fields= [ 'fecha']

class DocenteFilter(django_filters.FilterSet):
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model= Docentes
        fields= [ 'nombre','carrera']
  