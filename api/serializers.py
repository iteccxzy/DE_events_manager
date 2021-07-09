from rest_framework import serializers
from tuto.models import Carreras, Docentes, Horarios, Materias, Solicitudes


from django.db import models


class CarrerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carreras
        fields = '__all__'


class DocentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docentes
        fields = '__all__'


class HorariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horarios
        fields = '__all__'


class MateriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materias
        fields = '__all__'


class SolicitudesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitudes
        fields = '__all__'



class TsSerializer(serializers.ModelSerializer):
    carrera = serializers.StringRelatedField()
    materia = serializers.StringRelatedField()
    docente = serializers.StringRelatedField()
    horario = serializers.StringRelatedField()

    class Meta:
        model = Solicitudes
        fields = ['dia', 'carrera', 'materia', 'docente', 'horario']

