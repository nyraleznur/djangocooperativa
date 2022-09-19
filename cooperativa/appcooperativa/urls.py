from django.urls import path
from .views import ClienteViews
from .views import Creditosview
from .views import UsuarioViews
from . import views


urlpatterns=[

  path('login/cliente/',ClienteViews.as_view(), name="Listar"),
  path('cliente/<int:doc>',ClienteViews.as_view(), name="actualizar"),
  path('credito/',Creditosview.as_view(), name="Listar"),
  path('usuario/',UsuarioViews.as_view(), name="Listarusuarios"),
  path('login/',views.loginusuario, name="loginusu" ),
  path('gestioncliente',views.gestioncliente, name="gestion" ),
  path('login/frminsertar',views.frminsertar, name="registrar" ),
  

]