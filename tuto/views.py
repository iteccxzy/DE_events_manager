from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, User
from tuto.models import Docentes, Tutorias, Confirmaciones, Carreras, Materias, Perfiles, Solicitudes, Bimestres, Categorias, Canal
from tuto.forms import confirmaciones_Form, docentes_Form, carreras_Form, FormularioContacto, crearUserForm, PerfilForm, materias_Form
from tuto.decorators import *
from tuto.filters import TutoFilter, DocenteFilter
import datetime

from django.forms import inlineformset_factory

from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError

import xlwt
from django.db.models.functions import Concat
from django.db.models import Value

from django.db import connection

from django.urls import reverse

#--------------      login       --------------------------------####

@unauthenticated_user
def registerPage(request):
    form = crearUserForm()
    if request.method == 'POST':
        form = crearUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            nombre_usuario = form.cleaned_data.get('username')
            messages.success( request, 'cuenta creada     ' + nombre_usuario)            
 
            return redirect('login')
    context = {'form': form}
    return render(request, 'cuentas/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listar_tutorias')
        else:
            messages.info(request, 'usuario o pass incorrecto')
    context = {}
    return render(request, 'cuentas/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

#--------------- TUTORIAS   --------------------------------####

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listar_tutorias_v(request):

    myFilter= TutoFilter()
    if request.GET.get('fecha'):
        ts = Tutorias.objects.all().order_by('hora')
        myFilter= TutoFilter(request.GET, queryset=ts)
        ts= myFilter.qs
        fecha_e = request.GET.get('fecha')
        conf_ts = Tutorias.objects.select_related('confirmacion').filter(fecha=fecha_e, confirmacion__categoria=1).count()
        conf_ca = Tutorias.objects.select_related('confirmacion').filter(fecha=fecha_e, confirmacion__categoria=2).count()
        conf_me = Tutorias.objects.select_related('confirmacion').filter(fecha=fecha_e, confirmacion__categoria=3).count()
        conf_cu = Tutorias.objects.select_related('confirmacion').filter(fecha=fecha_e, confirmacion__categoria=4).count()
    else:
        ts = Tutorias.objects.filter(fecha=datetime.date.today()).order_by('hora')
        conf_ts = Tutorias.objects.select_related('confirmacion').filter(fecha=datetime.date.today(), confirmacion__categoria=1).count()
        conf_ca = Tutorias.objects.select_related('confirmacion').filter(fecha=datetime.date.today(), confirmacion__categoria=2).count()
        conf_me = Tutorias.objects.select_related('confirmacion').filter(fecha=datetime.date.today(), confirmacion__categoria=4).count()
        conf_cu = Tutorias.objects.select_related('confirmacion').filter(fecha=datetime.date.today(), confirmacion__categoria=6).count()

    
    context = {'Tutorias': ts, 'myFilter': myFilter, 'Conf_ts':conf_ts, 'Conf_ca':conf_ca, 'Conf_me':conf_me, 'Conf_cu':conf_cu}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def nueva_tutoria_v(request):
    if request.method == 'POST':
        form = confirmaciones_Form(request.POST)
        if form.is_valid():
            form.save()    
        return HttpResponseRedirect(reverse('listar_tutorias'))
    else:
        form = confirmaciones_Form()
    return render(request, 'nueva_ts.html', {'form': form})

#--------------- DOCENTES       --------------------------------####

@login_required(login_url='login')
def listar_docentes_v(request):
    docentes = Docentes.objects.all().order_by('docente_id')
    myFilter= DocenteFilter(request.GET, queryset=docentes)
    docentes= myFilter.qs
    context = {'Docentes': docentes, 'myFilter': myFilter}
    return render(request, 'docentes/docentes.html', context)

@login_required(login_url='login')
def nuevo_docentes_v(request):
    if request.method == 'POST':
        form = docentes_Form(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('listar_docentes'))

    else:
        form = docentes_Form()
    return render(request, 'docentes/docentes_form.html', {'form': form})

@admin_only
@login_required(login_url='login')
def nuevo_docente_c_v(request, carrera_id):
    DFormSet = inlineformset_factory(Carreras, Docentes, fields=('nombre', 'apellidos'), extra=3 )
    carrera = Carreras.objects.get(carrera_id=carrera_id)
    formset = DFormSet(queryset=Docentes.objects.none(),instance=carrera)
    if request.method == 'POST':
        formset = DFormSet(request.POST, instance=carrera)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'docentes/docentes_carrera.html', context)

@login_required(login_url='login')
def editar_docente_v(request, docente_id):
    docente = Docentes.objects.get(docente_id=docente_id)
    if request.method == 'GET':
        form = docentes_Form(instance=docente)
    else:
        form = docentes_Form(request.POST, instance=docente)
        if form.is_valid():
            form.save()
        return redirect('listar_docentes')
    return render(request, 'docentes/docentes_form.html', {'form': form})

@login_required(login_url='login')
def eliminar_docente_v(request, docente_id):
    docente = Docentes.objects.get(docente_id=docente_id)
    if request.method == 'POST':
        try:
            docente.delete()            
            return redirect('listar_docentes')
        except IntegrityError as e:
            context = {"message": str(e)}
            return render(request, "error_db.html", context)
    context =  {'Item': docente}
    return render(request, 'docentes/docentes_delete.html', context)

#--------------- CARRERAS       --------------------------------####

@login_required(login_url='login')
def listar_carreras_v(request):
    carreras = Carreras.objects.all().order_by('carrera_id')
    context = {'Carreras': carreras}
    return render(request, 'carreras/carreras.html', context)

@login_required(login_url='login')
def nueva_carreras_v(request):
    if request.method == 'POST':
        form = carreras_Form(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('listar_carreras'))

    else:
        form = carreras_Form()
    return render(request, 'carreras/carreras_form.html', {'form': form})

@login_required(login_url='login')
def editar_carrera_v(request, carrera_id):
    carrera = Carreras.objects.filter(carrera_id=carrera_id).first()
    if request.method == 'GET':
        form = carreras_Form(instance=carrera)
    else:
        form = carreras_Form(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
        return redirect('listar_carreras')
    return render(request, 'carreras/carreras_form.html', {'form': form})

@login_required(login_url='login')
def eliminar_carrera_v(request, carrera_id):
    carrera = Carreras.objects.get(carrera_id=carrera_id)
    if request.method == 'POST':
        try:
            carrera.delete()            
            return redirect('listar_carreras')
        except IntegrityError as e:
            context = {"message": str(e)}
            return render(request, "error_db.html", context)
    context =  {'Item': carrera}
    return render(request, 'carreras/carreras_delete.html', context)

## ----------- contacto -------##

def contacto(request):
  
    return render(request, 'contacto.html', {'form': {}})
    


#---------------------  vistas ajax         --------------------------------####

def load_materias(request):
    carrera_id = request.GET.get('carrera')
    materias = Materias.objects.filter(carrera=carrera_id)
    return render(request, 'dd_materias.html', {'materias': materias})

def load_docentes(request):
    carrera_id = request.GET.get('carrera')
    docentes = Docentes.objects.filter(carrera=carrera_id)
    return render(request, 'dd_docentes.html', {'docentes': docentes})

def save_resultado(request):
    t_id = request.GET.get('tuto')
    r_id = request.GET.get('value')
    m = Tutorias.objects.filter(tutoria_id=t_id).update(resultado=r_id)
    return HttpResponse(status=204)
##---------------------    perfil    ------------------------------- ##

@login_required(login_url='login')
def perfil(request):
    perfil = request.user.perfiles
    form = PerfilForm(instance=perfil)
    if request.method=='POST':
        form= PerfilForm(request.POST, request.FILES, instance= perfil)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('perfil'))

    context={'form':form}
    return render(request, 'perfil.html', context)


##---------------------    manejo de error    ------------------------------- ##

def handler404(request, exception):
    return render(request, '404.html')

##---------------------    exportar a excel    ------------------------------- ##

def export_events_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="eventos.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Eventos')

    numero_fila = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columnas = ['Carrera', 'Materia', 'Profesor', 'Fecha', 'Horario', 'Canal', 'Categoria' ]
    for columna in range(len(columnas)):
        ws.write(numero_fila, columna, columnas[columna], font_style)

    font_style = xlwt.XFStyle()
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    style2 = xlwt.easyxf(num_format_str='hh:mm')
    fech= request.GET.get('fech')
    rows = Tutorias.objects.select_related(
    'confirmacion',
    'confirmacion__carrera',
    'confirmacion__materia',
    'confirmacion__docente',
    'confirmacion__canal',
    'confirmacion__categoria'    
    ).filter(fecha=fech).values_list(
    'confirmacion__carrera__descripcion', 
    'confirmacion__materia__descripcion', 
    Concat('confirmacion__docente__nombre', Value(' '),'confirmacion__docente__apellidos'), 
    'fecha',
    'hora',
    'confirmacion__canal__descripcion',
    'confirmacion__categoria__descripcion' )

    for row in rows:
        numero_fila += 1
        for columna in range(len(row)):
            if columna == 3:
                 ws.write(numero_fila, columna, row[columna], style1)
            elif columna==4:
                ws.write(numero_fila, columna, row[columna], style2)            
            else:
                ws.write(numero_fila, columna, row[columna], font_style)
    wb.save(response)
    return response


@login_required(login_url='login')
def export_docentes_xls(request):
   
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="docentes.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Docentes')

    numero_fila = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columnas = ['Nombre', 'apellido', 'carrera' ]
    for columna in range(len(columnas)):
        ws.write(numero_fila, columna, columnas[columna], font_style)

    font_style = xlwt.XFStyle()

    c = connection.cursor()
    try:
        c.callproc("docentes_all")
        rows = c.fetchall()
    finally:
        c.close()

    for row in rows:
        numero_fila += 1
        for columna in range(len(row)):
            ws.write(numero_fila, columna, row[columna], font_style)
    wb.save(response)
    return response
    
#--------------- MATERIAS       --------------------------------####

@login_required(login_url='login')
def listar_materias_v(request):
    materias = Materias.objects.all().order_by('materia_id')
    context = {'Materias': materias}
    return render(request, 'materias/materias.html', context)

@login_required(login_url='login')
def nueva_materia_v(request):
    if request.method == 'POST':
        form = materias_Form(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('listar_materias'))

    else:
        form = materias_Form()
    return render(request, 'materias/materias_form.html', {'form': form})

@admin_only
@login_required(login_url='login')
def materia_c_v(request, carrera_id):
    DFormSet = inlineformset_factory(Carreras, Materias, fields=('descripcion', ), extra=3 )
    carrera = Carreras.objects.get(carrera_id=carrera_id)
    formset = DFormSet()
    if request.method == 'POST':
        formset = DFormSet(request.POST, instance=carrera)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'materias/materias_carrera.html', context)

@login_required(login_url='login')
def editar_materia_v(request, materia_id):
    materia = Materias.objects.get(materia_id=materia_id)
    if request.method == 'GET':
        form = materias_Form(instance=materia)
    else:
        form = materias_Form(request.POST, instance=materia)
        if form.is_valid():
            form.save()
        return redirect('listar_materias')
    return render(request, 'materias/materias_form.html', {'form': form})

@login_required(login_url='login')
def eliminar_materia_v(request, materia_id):
    materia = Materias.objects.get(materia_id=materia_id)
    if request.method == 'POST':
        try:
            materia.delete()            
            return redirect('listar_materias')
        except IntegrityError as e:
            context = {"message": str(e)}
            return render(request, "error_db.html", context)
    context =  {'Item': materia}
    return render(request, 'materias/materias_delete.html', context)

#--------------- requirement       --------------------------------####

@login_required(login_url='login')
def req_event(request):
    sol= Solicitudes.objects.filter(proc__isnull=True)
    canal= Canal.objects.all()
    bim= Bimestres.objects.all()
    categoria= Categorias.objects.all()
    context= {'sol':sol, 'canal':canal, 'bim':bim, 'categoria':categoria}
    return render(request, 'requirement.html', context)

def req_save(request):
    carrera= int(request.GET.get("carrera"))
    materia= int(request.GET.get("materia"))
    docente= int(request.GET.get("docente"))
    horario=  str(request.GET.get("horario"))
    fecha= datetime.datetime.strptime(request.GET.get("fecha"), '%Y-%m-%d').date()
    bim= int(request.GET.get("bim"))
    canal= int(request.GET.get("canal"))
    categ= int(request.GET.get("categ"))
    solid= request.GET.get('solid')
    
    m = Solicitudes.objects.filter(solicitud_id=solid).update(proc=True)

    c = connection.cursor()
    try:
        c.execute("BEGIN")
        c.execute("CALL insert_conf('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}');".format(carrera, materia, docente, horario, fecha, bim, canal, categ))

       
        c.execute("COMMIT")
    finally:
        c.close()

    return HttpResponse(status=204)