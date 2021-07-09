from django.contrib import admin
from tuto.models import Carreras, Docentes, Materias, Perfiles


class CarrerasAdmin(admin.ModelAdmin):
    search_fields = ("descripcion",)
    readonly_fields = ("carrera_id",)


class MateriasAdmin(admin.ModelAdmin):
    readonly_fields = ("materia_id",)


class DocentesAdmin(admin.ModelAdmin):
    readonly_fields = ("docente_id",)


admin.site.register(Carreras, CarrerasAdmin)
admin.site.register(Docentes, DocentesAdmin)
admin.site.register(Materias, MateriasAdmin)
admin.site.register(Perfiles)

