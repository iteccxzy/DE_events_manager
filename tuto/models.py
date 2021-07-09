from django.db import models
from django.contrib.auth.models import User


class Perfiles(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    foto =models.ImageField(default="profile.png",null=True, blank=True, upload_to='fotos')

    def __str__(self):
        return '%s' % (self.nombre)

    class Meta:
        verbose_name_plural = "Perfiles"


class Bimestres(models.Model):
    bim_id = models.AutoField(primary_key=True)
    agno = models.IntegerField()
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % (self.descripcion)


class Canal(models.Model):
    canal_id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % (self.descripcion)


class Carreras(models.Model):
    carrera_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, verbose_name="carrera")

    def __str__(self):
        return '%s' % (self.descripcion)

    class Meta:
        verbose_name_plural = "Carreras"


class Docentes(models.Model):
    docente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    carrera = models.ForeignKey('Carreras', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)

    class Meta:
        verbose_name_plural = "Docentes"


class Duraciones(models.Model):
    duracion_id = models.IntegerField(primary_key=True)
    cantidad_bimestres = models.IntegerField()


class Horarios(models.Model):
    horario_id = models.IntegerField(primary_key=True)
    hora = models.TimeField()

    def __str__(self):
        hora = (str(self.hora)[:5])
        return '%s' % hora


class Materias(models.Model):
    materia_id = models.AutoField(primary_key=True)
    carrera = models.ForeignKey('Carreras', models.DO_NOTHING, blank=True, null=True)
    descripcion = models.CharField(max_length=255, verbose_name="materia")

    def __str__(self):
        return '%s' % (self.descripcion)

    class Meta:
        verbose_name_plural = "Materias"


class Resultados(models.Model):
    resultado_id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % (self.descripcion)

class Categorias (models.Model):
    categoria_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % (self.descripcion)

class Confirmaciones(models.Model):
    confirmacion_id = models.AutoField(primary_key=True)

    carrera = models.ForeignKey(Carreras,     models.DO_NOTHING)
    materia = models.ForeignKey(Materias,     models.DO_NOTHING)
    horario = models.ForeignKey(Horarios,     models.DO_NOTHING, blank=True, null=True)
    docente = models.ForeignKey(Docentes,     models.DO_NOTHING)
    bimestre = models.ForeignKey(Bimestres,   models.DO_NOTHING)
    canal = models.ForeignKey(Canal,          models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING, blank=True, null=True)
    duracion = models.ForeignKey(Duraciones,  models.DO_NOTHING, blank=True, null=True)

    fecha_inicio = models.DateField(blank=True, null=True)
    hs = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Confirmaciones"

class Tutorias(models.Model):
    tutoria_id = models.AutoField(primary_key=True)

    confirmacion = models.ForeignKey(Confirmaciones,  on_delete=models.CASCADE)
    resultado = models.ForeignKey(Resultados,    models.DO_NOTHING, blank=True, null=True)
    
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)

# para api

class Solicitudes(models.Model):
    solicitud_id = models.AutoField(primary_key=True)
    
    carrera = models.ForeignKey(Carreras,    on_delete=models.CASCADE, related_name="solicitud_carrera")
    materia = models.ForeignKey(Materias,    on_delete=models.CASCADE, related_name="solicitud_materia")
    horario = models.ForeignKey(Horarios,    on_delete=models.CASCADE, related_name="solicitud_horario")
    docente = models.ForeignKey(Docentes,    on_delete=models.CASCADE, related_name="solicitud_docente")
    
    dia = models.CharField(max_length=255, verbose_name="dia")

    proc = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "solicitudes"
