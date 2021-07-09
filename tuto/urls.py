from django.urls import path
from tuto import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.listar_tutorias_v, name='listar_tutorias'),
    path('nueva_tutoria/', views.nueva_tutoria_v,  name='nueva_tutoria'),

    path('listar_docentes/', views.listar_docentes_v, name='listar_docentes'),
    path('nuevo_docente/', views.nuevo_docentes_v, name='nuevo_docente'),
    path('editar_docente/<int:docente_id>/',
         views.editar_docente_v, name='editar_docente'),
     path('eliminar_docente/<int:docente_id>/',
         views.eliminar_docente_v, name='eliminar_docente'),
    path('nuevo_docente_c_v/<int:carrera_id>/',
         views.nuevo_docente_c_v, name='nuevo_docente_c_v'),

    path('listar_carreras/', views.listar_carreras_v, name='listar_carreras'),
    path('nueva_carrera/', views.nueva_carreras_v, name='nueva_carrera'),
    path('editar_carrera/<int:carrera_id>/',
         views.editar_carrera_v, name='editar_carrera'),
     path('eliminar_carrera/<int:carrera_id>/',
         views.eliminar_carrera_v, name='eliminar_carrera'),

    path('load_materias/', views.load_materias, name='load_materias'),
    path('load_docentes/', views.load_docentes, name='load_docentes'),
    path('save_resultado/', views.save_resultado, name='save_resultado'),

    path('contact/', views.contacto, name='contact'),


    path('perfil/', views.perfil, name='perfil'),

    path('listar_materias/', views.listar_materias_v, name='listar_materias'),
    path('nueva_materia/', views.nueva_materia_v, name='nueva_materia'),
    path('editar_materia/<int:materia_id>/',
         views.editar_materia_v, name='editar_materia'),
     path('eliminar_materia/<int:materia_id>/',
         views.eliminar_materia_v, name='eliminar_materia'),

    path('materia_c_v/<int:carrera_id>/', views.materia_c_v, name='materia_c_v'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="cuentas/reset_password.html", 
    email_template_name="cuentas/reset_password_email.html"), name="reset_password"),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="cuentas/reset_password_sent.html"), 
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="cuentas/reset_password_form.html"), 
     name="password_reset_confirm"),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="cuentas/reset_password_done.html"), 
        name="password_reset_complete"),

    path('export_events_xls', views.export_events_xls, name="export_events_xls"),
    path('export_docentes_xls', views.export_docentes_xls, name="export_docentes_xls"),

    path('req_event', views.req_event, name="req_event"),
    path('req_save', views.req_save, name="req_save"),
    

]

