from rest_framework import generics

from tuto.models import Carreras, Materias, Horarios, Docentes, Solicitudes
from .serializers import CarrerasSerializer, MateriasSerializer, HorariosSerializer, DocentesSerializer, SolicitudesSerializer, TsSerializer



class DocentesList(generics.ListAPIView):
    queryset = Docentes.objects.all()
    serializer_class = DocentesSerializer



class SingleMaterias(generics.ListAPIView):
    serializer_class = MateriasSerializer

    def get_queryset(self, *args, **kwargs):
        """
        This view should return a list ....
        """
        carrera_id = self.kwargs["pk"]
        return Materias.objects.filter(carrera=carrera_id)


class HorariosList(generics.ListAPIView):
    queryset = Horarios.objects.all()
    serializer_class = HorariosSerializer



class MateriasList(generics.ListAPIView):
    queryset = Materias.objects.all()
    serializer_class = MateriasSerializer


class CarrerasList(generics.ListAPIView):
    queryset = Carreras.objects.all()
    serializer_class = CarrerasSerializer


class Solicitudes_Save(generics.CreateAPIView):
    queryset = Solicitudes.objects.all()
    serializer_class = SolicitudesSerializer



class TsList(generics.ListAPIView):
    queryset = Solicitudes.objects.all().select_related("carrera","materia", "docente", "horario").filter(proc=None)
    serializer_class = TsSerializer

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        from django.db import connection
        print('Numero de consultas: {}'.format(len(connection.queries)))
        return response
    



