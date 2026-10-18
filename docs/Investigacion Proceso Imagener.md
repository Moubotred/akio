REDIRECCION DE FOTOS SAD A LOCAL

empezamos buscando el archivo xml de la UI 
hacemos un pequena modificacion para ver como 

posible error cuando se aplique la modicacion activity_sst_foto.xml
puede que se bloque porque no otra de la views hace una conexion
a un servidor haciendo solicitudes y si no responder correctamente se 
bloqueara 

los archivos :

    fragment_inicio.xml  
        |_* contiene el la referencias de la view cuando inicia la app
            este es la represaracion grafica en ascci

            (fragment_inicio.xml) -> (InicioFragment.java) -> (InicioFragment.smali)

                ╔════════════════════════════════════════╗
                ║          CUADRILLA CATASTRO            ║
                ╠════════════════════════════════════════╣
                ║                                        ║
                ║   ┌────────────────────────────────┐   ║
                ║   │           CUADRILLA            │   ║
                ║   ├────────────────────────────────┤   ║
                ║   │  Tipo:    Cuadrilla Catastro   │   ║
                ║   │  Fecha:   06/10/2025 15:55     │   ║
                ║   └────────────────────────────────┘   ║
                ║                                        ║
                ║   ┌──────────────┐   ┌─────────────┐   ║
                ║   │ PENDIENTES   │   │ ATENDIDOS   │   ║
                ║   ├──────────────┤   ├─────────────┤   ║
                ║   │    12021     │   │      0      │   ║
                ║   └──────────────┘   └─────────────┘   ║
                ║                                        ║
                ║   ┌────────────────────────────────┐   ║
                ║   │         FINALIZAR JORNADA      │   ║
                ║   └────────────────────────────────┘   ║
                ║                                        ║
                ║        [👥]               [🔄]         ║
                ║     Seleccionar        Actualizar      ║
                ║      Cuadrilla                         ║
                ╚════════════════════════════════════════╝

    activity_sst_foto.xml 
        |_* contiene la refencia de como se etiqueta una foto
            cuando se sube una foto al servidor o se almacena
            en una base de datos local

            (activity_sst_foto.xml) -> (FotoActivity.java) -> (FotoActivity.smali)

            ┌────────────────────────────────────┐
            │ [X]          FOTO                  │
            ├────────────────────────────────────┤
            │                                    │
            │        ┌───────────────┐           │
            │        │      🖼️       │           │
            │        │   Añadir Foto │           │
            │        └───────────────┘           │
            │                                    │
            │ Tipo:    [▼] [cargando tipo...]    │
            │                                    │
            │ Subtipo: [▼] [cargando subtipo...] │
            │                                    │
            │ Comentario:                        │
            │                                    │
            │    [_________________________]     │
            │                                    │
            │         [   AGREGAR   ]            │
            │                                    │
            └────────────────────────────────────┘


    * ahora necesito saber como llegar hasta la view de activity_sst_foto.xml
    porque cuando se borra se instala la app modificada e inicia y carga 
    (InicioFragment.java) hace consultas como generar 
        como:


            CUADRILLA 
            PENDIENTE
            FECHA
            ACTULIZAR
            TIPO
            FINALIZAR JORNADA 
            ACTULIZAR
            SELECCIONAR CUADRILLA
            ATENDIDOS

        este es un json generado por la IA las cuales son las constates 
        web que se hacen al iniciar al parecer:
            {
                "consultas_web": [
                    {
                    "variable": "ParametroPlanificacionDto",
                    "linea": "parametroPlanificacionDto = new ParametroPlanificacionDto()",
                    "funcion": "ObtenerListadoSSTPlanificadas",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "/api/sst/planificadas",
                    "parametros": [
                        "tokenFCM",
                        "imei", 
                        "tipoAtencion",
                        "aplicacion",
                        "cuadrillaAtencion"
                    ]
                    },
                    {
                    "variable": "listadoTipoAtencion",
                    "linea": "this.listadoTipoAtencion = new Proxy().ObtenerTipoAtencionProveedorConCuadrillas",
                    "funcion": "ObtenerTipoAtencionProveedorConCuadrillas",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "/api/tipos-atencion",
                    "parametros": [
                        "Util.ObtenerTokenLDS(contextNullSafe)"
                    ]
                    },
                    {
                    "variable": "JornadaDto",
                    "linea": "JornadaDto jornadaDto = new JornadaDto()",
                    "funcion": "IniciarJornada",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "/api/jornada/iniciar",
                    "parametros": [
                        "cuadrilla",
                        "proveedor",
                        "imeiCapataz",
                        "tipoAtencion", 
                        "latitud",
                        "longitud"
                    ]
                    },
                    {
                    "variable": "JornadaDto",
                    "linea": "JornadaDto jornadaDto = new JornadaDto()",
                    "funcion": "MarcarSalidaDeBase",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "/api/jornada/salida-base",
                    "parametros": [
                        "cuadrilla",
                        "proveedor",
                        "imeiCapataz",
                        "tipoAtencion",
                        "latitud",
                        "longitud"
                    ]
                    },
                    {
                    "variable": "JornadaDto", 
                    "linea": "JornadaDto jornadaDto = new JornadaDto()",
                    "funcion": "MarcarRegresoABase",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "/api/jornada/regreso-base",
                    "parametros": [
                        "cuadrilla",
                        "proveedor",
                        "imeiCapataz",
                        "tipoAtencion",
                        "latitud",
                        "longitud"
                    ]
                    },
                    {
                    "variable": "JornadaDto",
                    "linea": "JornadaDto jornadaDto = new JornadaDto()",
                    "funcion": "FinalizarJornada",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "/api/jornada/finalizar",
                    "parametros": [
                        "cuadrilla",
                        "proveedor",
                        "imeiCapataz",
                        "tipoAtencion",
                        "latitud",
                        "longitud"
                    ]
                    },
                    {
                    "variable": "Proxy",
                    "linea": "Proxy proxy = new Proxy()",
                    "funcion": "Todas las consultas web",
                    "libreria": "com.luzdelsur.proydist.spocapataz.proxy.Proxy",
                    "endpoint": "Base URL configurada en Proxy",
                    "parametros": [
                        "URL base del servidor"
                    ]
                    },
                    {
                    "variable": "Util.ObtenerTokenLDS",
                    "linea": "Util.ObtenerTokenLDS(InicioFragment.this.contextNullSafe)",
                    "funcion": "Obtener token de autenticación",
                    "libreria": "com.luzdelsur.proydist.spocapataz.util.Util",
                    "endpoint": "N/A - Local storage",
                    "parametros": [
                        "contextNullSafe"
                    ]
                    },
                    {
                    "variable": "Util.ObtenerImei",
                    "linea": "Util.ObtenerImei(InicioFragment.this.contextNullSafe)",
                    "funcion": "Obtener IMEI del dispositivo",
                    "libreria": "com.luzdelsur.proydist.spocapataz.util.Util", 
                    "endpoint": "N/A - Dispositivo",
                    "parametros": [
                        "contextNullSafe"
                    ]
                    }
                ],
                "tareas_asyncronas": [
                    {
                    "clase": "CargaSSTAsignadasAsynk",
                    "metodo": "doInBackground",
                    "consultas": [
                        "ObtenerListadoSSTPlanificadas"
                    ]
                    },
                    {
                    "clase": "CargarDatosIniciales", 
                    "metodo": "doInBackground",
                    "consultas": [
                        "ObtenerTipoAtencionProveedorConCuadrillas"
                    ]
                    },
                    {
                    "clase": "IniciarJornadaTask",
                    "metodo": "doInBackground", 
                    "consultas": [
                        "IniciarJornada"
                    ]
                    },
                    {
                    "clase": "MarcarSalidaDeBaseTask",
                    "metodo": "doInBackground",
                    "consultas": [
                        "MarcarSalidaDeBase"
                    ]
                    },
                    {
                    "clase": "MarcarRegresoABaseTask",
                    "metodo": "doInBackground",
                    "consultas": [
                        "MarcarRegresoABase"
                    ]
                    },
                    {
                    "clase": "FinalizarJornadaTask",
                    "metodo": "doInBackground",
                    "consultas": [
                        "FinalizarJornada"
                    ]
                    }
                ]
                }

        * ahora sabemo que al iniciar pide paramatros web 
		  pero cual es el que pide la iniciar 
			
		  resulta que cuando interceptamos burpsuit hace un peticion a la
		  ruta :
				POST /tecnicoi/spo/sad/atencion/Atencion.svc/Atencion/ObtenerTipoAtencionCapataz HTTP/1.1

		  y buscame las palabras clave con grep ubicamos algunos archivos interesantes
		  donde genera la consulta
		  comandos grep:
						
						grep -rnsi 'ObtenerTipoAtencionCapataz' sources
						
						donde ubicamos el archivo URLServicios.java donde estan las constantes que son URLS
						
						ruta:
							sources/com/luzdelsur/proydist/spocapataz/util/URLServicios.java:21						
						
						res:
							URLServicios.java:21:public static String SERVICIO_OBTENER_TIPO_ATENCION_PROVEEDOR = "/Atencion/ObtenerTipoAtencionCapataz";

		luego aplicamos una busqueda con la constante de SERVICIO_OBTENER_TIPO_ATENCION_PROVEEDOR y ubicamos el archivo
		(Proxy.java:371) donde se usa esa constante 
		
		donde en la linea 371 de proxy.java hace una llamada a Restclient donde en la linea 374 hace un llamado POST
		y esa es la pimera llamada 

		pero ahora que URL DEBO MODIFICAR ?

		revisando la ejecucion de la app se queda bugeada cuando se inicia indetifique 
		que el archivo SplashActivity.java hace un llama web en la linea 151 el metodo
		se llama [ObtenerTipoInstanciaSAD] de la clase [Proxy.java] y recibe como argumeto 
		una llamada a Util.ObtenerTokenLDS(SplashActivity.this.getApplicationContext())
		donde llama a la clase [Util.java] y usa el metodo [ObtenerTokenLDS]
		donde se almacena en las preferencias :

		private static final String NOMBRE_ARCHIVO_PREFERENCIAS = "plataforma.movil.preferencias";        
	
		public static String ObtenerTokenLDS(Context context) {
            return context.getSharedPreferences(NOMBRE_ARCHIVO_PREFERENCIAS, 0).getString("TOKEN_AUTHLDS", "");
        }


        archivos relacionados para ubicar la primera llamada :
                                                            URLServicios.java - URL BASE
                                                            PostService.java - ENDPOINT
                                                            ServiceRetroFit.java - CONCATENACIÓN
                                                            Proxy.java - USO FINAL

        se hiso un curl para testear la url encotrada:

            curl -X POST "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerTipoInstanciaSAD" \
                -H "Content-Type: application/json" \
                -H "AuthLDS: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZU2tpZUI2NGdpeUZyM3hTMkVMVGROa3U3THlOU09zdnJteHp3SnhJSDdra3ViZmNJMyIsImlhdCI6IjE3NTk3NzU2MzAiLCJleHAiOiIxNzkxMzExNjMwIn0.EqCtgIpsDG0FOYt1F_Ou1R_81R5y3kxSgzAia1uu_wM" \
                -d '{"jornadaDto": null}' \
                -v

        esta es la primera llamada 

        URLServicios.URL_SERVICIO = "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/capataz/Capataz.svc"
        +
        ServiceRetroFit concatena: "/" 
        +
        PostService endpoint: "Capataz/ObtenerTipoInstanciaSAD"
        =
        URL FINAL: "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerTipoInstanciaSAD"



		

esta solicitus es como la segunad pero esta sin la intercepta burpsuit 

curl -o ObtenerSSTMiPlanificacion.json -X POST "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerSSTMiPlanificacion" \
  -H "Content-Type: application/json" \
  -H "AuthLDS: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZU2tpZUI2NGdpeUZyM3hTMkVMVGROa3U3THlOU09zdnJteHp3SnhJSDdra3ViZmNJMyIsImlhdCI6IjE3NTk3NzU2MzAiLCJleHAiOiIxNzkxMzExNjMwIn0.EqCtgIpsDG0FOYt1F_Ou1R_81R5y3kxSgzAia1uu_wM" \
  -d '{"parametroDto":{"aplicacion":"com.luzdelsur.proydist.sad","imei":"9657cc54ad670e5b","porcentajeAvanceCero":false,"tipoAtencion":"SACATASTRO"}}' \
  -v 


enlace de deepseeke que ayudo a desarollar el script de proxy para la intercepcion de trafico de solicitudes 
https://chat.deepseek.com/a/chat/s/9687c79f-82b6-48fa-9f04-df0a4d875c22

ya se logro la intercepcion de las solicitudes con la modificacion de las constantes de URLServicios.java 

con el script activo recive envia y responde a las solicitudes para ver los json generados



este curl ayuda a ver los tipos de fotos que pide el sad en cada suministro
los paramtros como  -d '{"tipoAtencion":"SACATASTRO","idAtencionCapataz":"17549157"}'
se obtiene de la llamada anterior con curl de ObtenerSSTMiPlanificacion y da un json 
con paramtros pero usando grep , sed , head , buscarmos las lineas donde estan los 
parantros {"tipoAtencion":"SACATASTRO","idAtencionCapataz":"17549157"} y los usamos 
para el siguiente curl el cual no indica que tipo de fotos podemos subir 

curl -v -o ObtenerTipoDocumentoPorAtencion.json -X POST "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/sad/archivo/Archivo.svc/Archivo/ObtenerTipoDocumentoPorAtencion" \
  -H "Content-Type: application/json" \
  -H "AuthLDS: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZU2tpZUI2NGdpeUZyM3hTMkVMVGROa3U3THlOU09zdnJteHp3SnhJSDdra3ViZmNJMyIsImlhdCI6IjE3NTk3NzU2MzAiLCJleHAiOiIxNzkxMzExNjMwIn0.EqCtgIpsDG0FOYt1F_Ou1R_81R5y3kxSgzAia1uu_wM" \
  -d '{"tipoAtencion":"SACATASTRO","idAtencionCapataz":"17549157"}'


ahora como se sube la foto ?

* el encargado de subir la fotos hacia el servidor es TareaAsynkTask.java
	que usa el metodo de [doInBackground] este es el flujo completo de envio

	Foto2Activity.AgregarFotoSST()

    → RSSPullService 
    → TareaEventosAsynkTask 
    → TareaAsynkTask.doInBackground()
        → Obtiene fotos pendientes (DAO.ObtenerListadoFotosPendientesCargar())
        → Para cada foto:
            - Lee archivo como bytes[]
            - Crea DTO con metadatos
            - Ejecuta proxy.AgregarImagen() o proxy.AgregarImagenRequisito()
            - Actualiza estado a 2 (subido)


https://chat.deepseek.com/a/chat/s/0ffa0dfb-12bc-4fae-bdbd-6e2e8802f4cf






curl -i -X POST "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/sad/archivo/Archivo.svc/Archivo/AgregarDocumento" \
  -H "AuthLDS: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZU2tpZUI2NGdpeUZyM3hTMkVMVGROa3U3THlOU09zdnJteHp3SnhJSDdra3ViZmNJMyIsImlhdCI6IjE3NTk3NzU2MzAiLCJleHAiOiIxNzkxMzExNjMwIn0.EqCtgIpsDG0FOYt1F_Ou1R_81R5y3kxSgzAia1uu_wM" \
  -H "Content-Type: multipart/form-data" \
  -F "imagen=@/home/kimshizi/Images/png/animacion.png;type=image/png" \
  -F "metadata={\"codigoAtencion\":\"AT20241007\",\"nombreArchivo\":\"animacion.png\",\"nroEmpresa\":\"7\",\"descripcion\":\"Foto\",\"latitud\":-12.046374,\"longitud\":-77.042793,\"subTipo\":\"FOADC\",\"idAtencionCapataz\":\"17549157\",\"tipoArchivo\":\"FO\",\"idSubtipoDocumento\":\"\",\"idDocLocal\":\"999\"};type=application/json"


curl -v -X POST "https://zsp1.luzdelsur.com.pe/tecnicoi/spo/sad/archivo/Archivo.svc/Archivo/AgregarDocumento" \
  -H "AuthLDS: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZU2tpZUI2NGdpeUZyM3hTMkVMVGROa3U3THlOU09zdnJteHp3SnhJSDdra3ViZmNJMyIsImlhdCI6IjE3NTk3NzU2MzAiLCJleHAiOiIxNzkxMzExNjMwIn0.EqCtgIpsDG0FOYt1F_Ou1R_81R5y3kxSgzAia1uu_wM" \
  -H "Content-Type: multipart/form-data" \
  -F "imagen=@/home/kimshizi/Images/png/animacion.png;type=image/png" \
  -F "metadata={\"codigoAtencion\":\"AT20241007\",\"nombreArchivo\":\"animacion.png\",\"nroEmpresa\":\"7\",\"descripcion\":\"Foto\",\"latitud\":-12.046374,\"longitud\":-77.042793,\"subTipo\":\"FOADC\",\"idAtencionCapataz\":\"17549157\",\"tipoArchivo\":\"FO\",\"idSubtipoDocumento\":\"\",\"idDocLocal\":\"999\"};type=application/json"


/Archivo/AgregarDocumento