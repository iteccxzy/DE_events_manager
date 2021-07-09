from django.urls import path
from api.apiviews import CarrerasList, MateriasList, SingleMaterias, HorariosList, DocentesList, Solicitudes_Save, TsList
from api import views


urlpatterns = [


    path('carreras/', CarrerasList.as_view(), name='carreras'),
    path('materias/', MateriasList.as_view(), name='materias'),
    path('smateria/<int:pk>', SingleMaterias.as_view(), name='materias'),
    path('horarios/', HorariosList.as_view(), name='horarios'),
    path('docentes/', DocentesList.as_view(), name='docentes'),
    path('solicitudes/', Solicitudes_Save.as_view(), name='solicitudes'),
    path('ts/', TsList.as_view(), name='ts')
]
