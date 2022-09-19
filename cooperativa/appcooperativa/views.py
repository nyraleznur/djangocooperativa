from calendar import c
from email import message
import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from .models import Cliente
from .models import Credito
from .models import Lineas_De_Credito
from .models import Usuario

from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class ClienteViews(View):
 @method_decorator(csrf_exempt)
 def dispatch(self,request,*args,**kwargs):
      return super().dispatch(request,*args,**kwargs)
 #@login_required
 
 def get(self,request,doc=0):
   
   if doc>0:
     cli=list(Cliente.objects.filter(documento=doc).values())
     if len(cli)>0:
      clirespuesta=cli[0]
      datos={"cliente":clirespuesta}
     else:
      datos={"respuesta":"Dato no se encontro"}
   else:
    template_name="consultarcli.html"
    cli=Cliente.objects.all()
    datos={'listadoclientes':cli}
   #return JsonResponse (datos)
   return render(request,template_name,datos)

 #@login_required
 def post(self,request):
    template_name="registrocliente.html"
    #datos=json.loads(request.body)
    Cliente.objects.create(documento=request.POST["documento"],nombre =request.POST["nombre"], apellido=request.POST["apellido"],correo=request.POST["correo"],celular=request.POST["celular"])
    return redirect('/login/cliente')

 def put(self,request,doc):
   datos=json.loads(request.body)
   cli=list(Cliente.objects.filter(documento=doc).values())
   if len(cli)>0:
    clientes=Cliente.objects.get(documento=doc)  
    clientes.nombre=datos['nombre']
    clientes.apellido=datos['apellido']
    clientes.correo=datos['correo']
    clientes.celular=datos['celular']
    clientes.save()
    mensaje={"Respuesta":"Datos actualizado"}
   else:
       mensaje={"Respuesta":"Datos no encontrado"}
   return JsonResponse(mensaje)

 def delete(self,request,doc):
      cli=list(Cliente.objects.filter(documento=doc).values())
      if len(cli)>0:
         Cliente.objects.filter(documento=doc).delete()
         mensaje={"Respuesta":"El registro se elimino"}
      else:
          mensaje={"Respuesta":"El registro no se encontro"}
      return JsonResponse (mensaje)

   
class Creditosview(View):
   @method_decorator(csrf_exempt)
   def  dispatch(self,request,*args,**kwargs):
      return super().dispatch(request,*args,**kwargs)

   def get(self,request):
      cre=list(Credito.objects.values())
      if  len(cre)>0:
         datos={"Datos":cre}
        # return JsonResponse(datos)
         return render(request, "gestionc.html",{"clientes":datos})
      else:
         datos={"Mensaje":"Dtaos no encontrador"}
      return JsonResponse(datos)
   
   def post(self,request):
      datos=json.loads(request.body)
      try:
         linea=Lineas_De_Credito.objects.get(codigo=datos["codigo"])
         cli=Cliente.objects.get(documento=datos["documento"])
         cre=Credito.objects.create(codigo_credito=datos["codigo_credito"],fecha=datos["fecha"],montoprestado =datos["montoprestado"],documento=cli,codigo=linea)
         cre.save()
         mensaje={"mensaje":"Guardado"}
       # Credito.objects.create( codigo_credito=datos["codigo_credito"],fecha=datos["fecha"],montoprestado =datos["montoprestado"], documento=datos["documento"],codigol=datos["codigo"])
         return JsonResponse(datos)
      except Cliente.DoesNotExist:
         mensaje={"mensaje":"La linea no existe"}
      except Lineas_De_Credito.DoesNotExist:
         mensaje={"mensaje":"clddddd"}
      return JsonResponse(mensaje)

class UsuarioViews(View):
 @method_decorator(csrf_exempt)
 def dispatch(self,request,*args,**kwargs):
      return super().dispatch(request,*args,**kwargs)

 def get(self,request,doc=0):
   if doc>0:
     cli=list(Usuario.objects.filter(documento=doc).values())
     if len(cli)>0:
      clirespuesta=cli[0]
      datos={"cliente":clirespuesta}
     else:
      datos={"respuesta":"Dato no se encontro"}
   else:
    cli=list(Usuario.objects.values())
    datos={'listadoclientes':cli}
   return JsonResponse (datos)


 def post(self,request):
    datos=json.loads(request.body)
    cli=Cliente.objects.get(documento=datos["documento"])
    Usuario.objects.create(Documento=datos["documento"],nomusuario=datos["nomusuario"],clave=datos["clave"],rol=datos["rol"],documento=cli)
                      
    return JsonResponse(datos)








def loginusuario(request):
      if request.method=='POST':
         try:
            detalleusuario=Usuario.objects.get(nomusuario=request.POST['nomusuario'], clave=request.POST['clave'])
            #detalleusuario=Cliente.objects.get(documento=['documento'], correo=['correo'])

            print("datosssssssssssss", detalleusuario.rol)
            if detalleusuario.rol=="admin":
               request.session['nomusuario']=detalleusuario.nomusuario
               return render(request, 'gestionc.html')
            elif detalleusuario.rol=="empleado":
               request.session['nomusuario']=detalleusuario.nomusuario
               return render(request, 'empleados.html')
            elif detalleusuario.rol=="cliente":
               request.session['nomusuario']=detalleusuario.nomusuario
               return render(request, 'clientes.html')   
         except Usuario.DoesNotExist as e:
            message.success(request,"No existe")
      return render(request,"login.html")


def gestioncliente(request):
   return render(request,"gestionc.html")

def frminsertar(request):
   return render(request,"registrocliente.html")



