from django import forms
from tuto.models import Confirmaciones, Docentes, Carreras, Materias, Perfiles
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfiles
		fields = '__all__'
		exclude = ['user']

class crearUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
     
class confirmaciones_Form(forms.ModelForm):
    class Meta:
        model = Confirmaciones

        fields = [
            'carrera',
            'materia',
            'docente',
            'hs',
            'fecha_inicio',
            'bimestre',
            'canal',
            'categoria',
        ]

        labels = {
            'carrera': 'Carrera',
            'materia': 'Materia',
            'docente': 'Docente',
            'hs': 'Horario',
            'fecha_inicio': 'Fecha de Inicio',
            'bimestre': 'Bimestre',
            'canal': 'Canal',
            'categoria': 'Categoria',
        }

        widgets = {
            'carrera':      forms.Select(attrs={'class': 'form-control form-control-sm '}),
            'materia':      forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'docente':      forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'hs':           forms. DateInput(attrs={'class': 'form-control form-control-sm','type':'time'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'bimestre':     forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'canal':        forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'categoria':    forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['carrera'].empty_label = ''
        self.fields['materia'].empty_label = ''
        self.fields['docente'].empty_label = ''
        self.fields['hs'].empty_label = ''
        self.fields['bimestre'].empty_label = ''
        self.fields['canal'].empty_label = ''
        self.fields['categoria'].empty_label = ''


class docentes_Form(forms.ModelForm):
    class Meta:
        model = Docentes

        fields = [
            'docente_id',
            'nombre',
            'apellidos',
            'carrera',
        ]

        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'carrera': 'Carrera'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'carrera': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].empty_label = ''
            
class carreras_Form(forms.ModelForm):
    class Meta:
        model = Carreras

        fields = [
            'carrera_id',
            'descripcion',
        ]

        labels = {
            'Materia': 'descripcion',
        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class FormularioContacto(forms.Form):
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "cols": 18, 'class': 'form-control form-control-sm'}))



class materias_Form(forms.ModelForm):
    class Meta:
        model = Materias

        fields = [
            'materia_id',
            'descripcion',
            'carrera',
        ]

        labels = {
            'descripcion': 'Materia',
             'carrera': 'Carrera',
        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'carrera': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].empty_label = ''