# 📘 Proxy IA Catastro

> [!WARNING]
> Este es un **proyecto experimental educativo** de Proxy IA (FastAPI + LLM) para automatizar el catastro eléctrico mediante fotografías.
> **No está afiliado oficialmente** a ninguna entidad eléctrica.
> Incluye análisis de código Smali de una suite de aplicaciones de un ecosistema cerrado, con fines únicamente de comprensión y optimización.
> El uso es estrictamente **educativo**

---

## 📑 Índice

- [Introducción](#-introducción)
- [Herramientas](#-herramientas)
- [Metodología de análisis](#-metodología-de-análisis)
- [Análisis por paquete](#-análisis-por-paquete)
  - [com.*.plataforma.movil](#-complataformamovil)
  - [com.*.proydist.sad](#-comproydistsad)
  - [com.*.bt.inspecciones.ui](#-combtinspeccionesui)
- [Procesamiento con LLM ](#-procesamiento-con-llm-gemini)
- [Despliegue de servidores](#-despliegue-de-servidores)
- [Uso](#-uso)
- [Características](#-características)
- [Conclusión](#-conclusión)

---

## 🧭 Introducción

**akio** es un servidor intermediario desarrollado con **Python**, **FastAPI** y un **LLM ** que procesa fotografías mediante inteligencia artificial para automatizar el catastro de suministros eléctricos, optimizando la extracción y organización de la información capturada en campo.

El proyecto se construyó de forma **iterativa e incremental**, validando cada capa antes de avanzar a la siguiente:

1. Estudio del login de la **plataforma base** y su dominio hardcodeado.
2. Redirección del dominio a un servidor HTTP mínimo de pruebas (`http.server`).
3. Réplica del endpoint final y comprensión de la generación de JWT.
4. Migración del servidor de prueba a **FastAPI**.
5. Estudio de la app **SAD** (catastro) con el mismo método: `grep` + reemplazo de URLs.
6. Mapeo del flujo `SST → paquete → catastro → foto → POST`.
7. Implementación del procesamiento con **Gemini** y validación de resultados.

---

## 🛠️ Herramientas

Herramientas destacadas durante el periodo de análisis:

| Comando | Descripción |
|---|---|
| `grep` | Busca cadenas dentro de archivos |
| `find` | Localiza directorios o archivos |
| `sed` | Procesa y transforma texto |
| `apktool` | Compila y descompila APKs |
| `jadx-gui` | Análisis parcial de código Java |
| `uber-apk-signer` | Firma automática de APKs |
| `ngrok` | Expone servidor local a internet |
| `adb` | Comunicación ordenador ↔ Android |
| `python` | Lenguaje de programación del servidor |

---

## 🔬 Metodología de análisis

Para el periodo de análisis se usó `apktool` para descompilar el código y `grep` para buscar URLs hardcodeadas en el código Smali. Estas URLs se reemplazaron por el túnel generado por `ngrok` al exponer un servidor local de Python.

**Comandos base:**

```bash
# Iniciar túnel de ngrok
ngrok http 5050

# Descompilar APK
apktool d app.apk -o smali/ -j 2

# Recompilar APK
apktool b smali/ -o app-rebuild.apk -j 2
```

**Búsqueda de URLs hardcodeadas:**

```bash
grep -rsni "https://" smali/
```

---

## 📦 Análisis por paquete

### 📱 com.*.plataforma.movil

Se descompiló el APK base con:

```bash
apktool d base.apk -o smali/ -j 2
```

La búsqueda `grep -rsni "https://"` arrojó múltiples coincidencias. Las líneas relevantes cuyo dominio fue reemplazado por el túnel de `ngrok` son:

| Archivo | Línea(s) |
|---|---|
| `ProxyPlataformaAplicacionesFactory.smali` | 52 |
| `ProxyPlataformaAplicacionesFactory.smali` | 127 |

**Recompilación e instalación:**

```bash
apktool b smali/ -o rebuild.apk -j 2
adb install rebuild.apk
```

**Servidor de pruebas en Python:**

```bash
python example.py 5050
```

Las rutas detectadas se dividen en tres fragmentos:

```
[zsp1.*.com.pe] [ /interno/platafadr/framework/lanzador/PltAndroid.svc ] [ Ruta ]
```

| Ruta | Prioridad |
|---|---|
| `/Login` | ✅ Alta |
| `/ValidaCredenciales` | ✅ Alta |
| `/ParametrosIniciales` | ✅ Alta |
| `/RegistroEjecucionAplicacion` | ⚠️ Media |
| `/ValidarSesionActivaImei` | ⚠️ Media |

Solo las **dos primeras rutas** resultaron prioritarias; las demás no devolvieron respuesta útil desde el servidor destino original.

---

### 📱 com.*.proydist.sad

Se aplicó la misma técnica: `grep` + `find` para localizar URLs y reemplazo del dominio por el túnel de `ngrok`.

**Líneas con dominio reemplazado:**

| Archivo | Línea(s) |
|---|---|
| `URLServicios.smali` | 43, 45, 47, 49, 51, 53, 55, 57, 59, 69, 71, 73 |
| `ServiceRetroFit.smali` | 107 |
| `ServicioFirebaseLDS.smali` | 18 |

#### 🌐 URLs de producción

| Campo | Valor |
|---|---|
| `URL_PRODUCCION` | `https://zsp1.*.com.pe/tecnicoi/spo/capataz/Capataz.svc` |
| `URL_PRODUCCION_ARCHIVO` | `https://zsp1.*.com.pe/tecnicoi/spo/sad/archivo/Archivo.svc` |
| `URL_PRODUCCION_ATENCION` | `https://zsp1.*.com.pe/tecnicoi/spo/sad/atencion/Atencion.svc` |
| `URL_SERVICIO_OCURRENCIA_PRODUCCION` | `https://zsp1.*.com.pe/tecnicoi/spo/sad/evento/evento.svc/` |

#### 🔗 Endpoints — `Capataz.svc`

| Constante | Endpoint |
|---|---|
| `SERVICIO_AGREGAR_ATENCION` | `/Capataz/AgregarAtencionCapataz` |
| `SERVICIO_AGREGAR_EVENTO` | `/Capataz/AgregarEvento` |
| `SERVICIO_AGREGAR_SST_EMERGENCIA` | `/Capataz/AgregarSSTEmergencia` |
| `SERVICIO_ASIGNAR_CUADRILLA_SAD` | `/Capataz/AsignarCuadrillaSad` |
| `SERVICIO_FINALIZAR_JORNADA` | `/Capataz/FinalizarJornada` |
| `SERVICIO_INICIAR_JORNADA` | `/Capataz/IniciarJornada` |
| `SERVICIO_OBTENER_CUADRILLA_TIPO_ATENCION` | `/Capataz/ObtenerCuadrillas` |
| `SERVICIO_OBTENER_DETALLE_ATENCION` | `/Capataz/ObtenerDetalleAtencion` |
| `SERVICIO_OBTENER_MENSAJE_ETAPA` | `/Capataz/ObtenerMensajePorEtapaToken` |
| `SERVICIO_OBTENER_SST_ASIGNADAS` | `/Capataz/ObtenerSSTMiPlanificacion` |
| `SERVICIO_OBTENER_SST_ASIGNADAS_SUPERVISION` | `/Capataz/ObtenerSSTMiPlanificacionSupervision` |
| `SERVICIO_OBTENER_SST_ASIGNADAS_TOTAL` | `/Capataz/ObtenerSSTMiPlanificacionTotal` |
| `SERVICIO_OBTENER_SUBTIPO_DOCUMENTO` | `/Capataz/ObtenerSubtipoDocumentoAtencion` |

#### 🔗 Endpoints — `Archivo.svc`

| Constante | Endpoint |
|---|---|
| `SERVICIO_AGREGAR_IMAGEN` | `/Archivo/AgregarDocumento` |
| `SERVICIO_AGREGAR_IMAGEN_EJECUTOR` | `/Archivo/AgregarDocumentoEjecutor` |

#### 🔗 Endpoints — `Atencion.svc`

| Constante | Endpoint |
|---|---|
| `SERVICIO_OBTENER_TIPO_ATENCION_PROVEEDOR` | `/Atencion/ObtenerTipoAtencionCapataz` |
| `SERVICIO_OBTENER_TIPO_ATENCION_SUPERVISOR` | `/Atencion/ObtenerTipoAtencionSupervisor` |

#### 🔗 Endpoints — `evento.svc`

| Constante | Endpoint |
|---|---|
| `SERVICIO_OCURRENCIA_AGREGAR_OCURRENCIA` | `/Evento/AgregarEvento` |

#### 🧩 Campos activos en runtime

Estos campos están vacíos en el `.class` y se llenan en ejecución según el ambiente:

- `URL_SERVICIO`
- `URL_SERVICIO_ARCHIVO`
- `URL_SERVICIO_ATENCION`
- `URL_SERVICIO_OCURRENCIA`

#### 📤 Flujo de subida de fotos (SAD)

```
TareaAsynkTask.java (doInBackground)
   → Proxy.java (AgregarImagen / AgregarImagenRequisito)
      → RestClientStream.java (EjecutarMetodoPOSTStream)
```

**Metadatos enviados en el `FotoDto`:**

```java
fotoDto.codigoAtencion     = foto.codigoAtencion;
fotoDto.nombreArchivo      = foto.nombre;
fotoDto.nroEmpresa         = "7";
fotoDto.descripcion        = foto.descripcion;
fotoDto.latitud            = foto.latitud;
fotoDto.longitud           = foto.longitud;
fotoDto.subTipo            = foto.tipo;
fotoDto.idAtencionCapataz  = foto.idAtencionCapataz;
fotoDto.tipoArchivo        = foto.tipoArchivo;
fotoDto.idSubtipoDocumento = foto.subTipoDocumento;
fotoDto.idDocLocal         = foto.idLogico;   // ← clave para CRUD local/remoto
```

#### 🧾 Conversión binario → JPG

La foto viaja como **binario bruto**. Los primeros bytes permiten identificar el formato:

```
FF D8 FF E0  →  JPG
```

**Conversión práctica:**

```bash
file name.bin      # identificar formato
mv name.bin imagen.jpg
```

---

### 📱 com.*.bt.inspecciones.ui

Búsqueda con `grep -rsni "https://"` sobre el código descompilado. Se identificaron dos URL base:

```
https://zsp1.*.com.pe | tecnicoii/GesManmtoBT/BTInspeccion.svc | <ruta>
https://zsp1.*.com.pe | tecnicoii/GesManmtoBT/BTCatastroWeb.svc | <ruta>
```

**Archivos con dominio reemplazado:**

| Archivo | Línea(s) |
|---|---|
| `ProxyBTConstants$Conexion.smali` | 18, 22, 24 |
| `ServiceFactory.smali` | 7, 9, 57, 144 |
| `FotoServiceFactory.smali` | 65 |

#### 🔗 Endpoints — Configuración

| Constante | Endpoint |
|---|---|
| `CONFIGURACION_CAJA_TOMA` | `configuracion/cajatoma` |
| `CONFIGURACION_LLAVE` | `configuracion/llave` |
| `CONFIGURACION_POSTE` | `configuracion/poste` |
| `CONFIGURACION_SUMINISTRO` | `configuracion/suministro` |
| `CONFIGURACION_VALIDA_FOTO` | `configuracion/valida/foto` |

#### 🔗 Endpoints — Usuario

| Constante | Endpoint |
|---|---|
| `OBTENER_DATOS_USUARIO` | `usuario` |

#### 🔗 Endpoints — Mapa / Paquetes de trabajo

| Constante | Endpoint |
|---|---|
| `AGREGAR_ACTIVO` | `mapa/agregaractivopaquetetrabajo` |
| `AGREGAR_ACTIVO_NN` | `mapa/agregaractivonnpaquetetrabajo` |
| `OBTENER_PAQUETES_INSPECCION` | `mapa/paquetesinspeccion` |
| `OBTENER_PAQUETES_TRABAJO` | `mapa/paquetestrabajo` |

#### 🔗 Endpoints — Capas del mapa

| Constante | Endpoint |
|---|---|
| `OBTENER_ACOMETIDAS` | `capa/acometidasdistancia` |
| `OBTENER_CLIENTES` | `capa/clientesregion` |
| `OBTENER_LAMPARAS` | `capa/lamparasregion` |
| `OBTENER_POSTE` | `capa/poste` |
| `OBTENER_POSTES` | `capa/postesregion` |
| `OBTENER_PUNTOS_SUMINISTROS` | `capa/puntossuministroregion` |
| `OBTENER_SUBESTACION` | `capa/subestacion` |
| `OBTENER_SUBESTACIONES` | `capa/subestacionesregion` |
| `OBTENER_TRAMOS` | `capa/tramosdistancia` |

#### 🔗 Endpoints — Activos

| Constante | Endpoint |
|---|---|
| `OBTENER_ACTIVO_POSICION` | `activo/posicion` |
| `OBTENER_GRADO_CORROSION` | `activo/poste/gradocorrosion` |
| `OBTENER_INFORMACION_POSTE` | `activo/poste` |
| `VALIDAR_ACTIVO_NN` | `activo/validaractivonn` |

#### 🔗 Endpoints — Inspección

| Constante | Endpoint |
|---|---|
| `ACTUALIZAR_ESTADO_INSPECCION` | `inspeccion/estado/actualizar` |
| `DESCARGAR_FOTO` | `inspeccion/descargarfoto` |
| `INSPECCION_DETALLE` | `inspeccion/detalle` |
| `OBTENER_FOTOS` | `inspeccion/fotos` |
| `OBTENER_INSPECCION_CAJA_TOMA` | `inspeccion/cajatoma` |
| `OBTENER_INSPECCION_LLAVE` | `inspeccion/llave` |
| `OBTENER_INSPECCION_POSTE` | `inspeccion/poste` |
| `OBTENER_INSPECCION_SUMINISTRO` | `inspeccion/suministro` |
| `OBTENER_TIPO_FOTOS` | `inspeccion/tipofotos` |
| `REGISTRAR_CNR` | `inspeccion/suministo/cnr` |
| `REGISTRAR_CODICION_RIESGO` | `inspeccion/suministo/condicionriesgo` |
| `REGISTRAR_EVENTO_SAD` | `inspeccion/evento/sad` |
| `REGISTRAR_INSPECCION_CAJA_TOMA` | `inspeccion/registrar/cajatoma` |
| `REGISTRAR_INSPECCION_LLAVE` | `inspeccion/registrar/llave` |
| `REGISTRAR_INSPECCION_POSTE` | `inspeccion/registrar/poste` |
| `REGISTRAR_INSPECCION_SUMINISTRO` | `inspeccion/registrar/suministro` |
| `SUBIR_FOTO` | `inspeccion/subirfoto` |

---

## 🤖 Procesamiento con LLM 

> ⚠️ **Sección en diseño.** Las rutas definitivas del LLM aún no están cerradas. A continuación se documenta el diseño propuesto.

### Flujo objetivo

```
[App móvil]
   │  POST multipart
   ▼
[Proxy FastAPI]
   │  Extrae metadatos Base64 + binario de imagen
   │  Valida token, MIME, tamaño
   ▼
[Gemini]
   │  Pre-prompt + imagen
   ▼
[Proxy FastAPI]
   │  Recibe JSON estructurado del catastro
   │  Valida reglas de negocio
   │  Calcula hash SHA-256 de la imagen
   ▼
[Respuesta al cliente]
   │  { ok, data, requiere_revision, estado_actualizado }
   ▼
[Servidor de destino]  ← reenvío con estado actualizado
```

### Pre-prompt propuesto (borrador)

```text
Eres un asistente experto en catastro eléctrico.
Analiza la imagen de mantenimiento y extrae:
- tipo_instalacion
- numero_medidor
- lectura
- poste
- transformador
- direccion_aproximada
- coordenadas
- observaciones
- confianza (0-1)

Devuelve SOLO JSON válido. Si un campo no se ve, usa null.
No inventes datos. No agregues texto fuera del JSON.
```

### Endpoint propuesto (borrador, no definitivo)

```http
POST /api/v1/cadastre/analizar
Content-Type: multipart/form-data
Authorization: Bearer <token>

file=@foto_medidor.jpg
metadata=<base64(json)>
```

### Pendiente por definir

- [ ] Ruta final del endpoint en el proxy.
- [ ] Esquema exacto de `metadata` (campos obligatorios vs. opcionales).
- [ ] Umbral de confianza para revisión humana.
- [ ] Persistencia del JSON resultante (PostgreSQL / SQLite).
- [ ] Reenvío al servidor de destino (`/Archivo/AgregarDocumento` o `/inspeccion/subirfoto`).
- [ ] Manejo de errores y reintentos.
- [ ] Autenticación de extremo a extremo (JWT).
- [ ] Auditoría (usuario, hora, hash de imagen, resultado).

---

## 🚀 Despliegue de servidores

### 1. Servidor de datos estáticos

Ingresamos al directorio `Local` y generamos certificados de prueba:

```bash
cd Local/
ls

openssl req -x509 -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -sha256 -days 365 \
  -nodes \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

Iniciamos el servidor con HTTPS:

```bash
uvicorn server:app --reload \
  --ssl-keyfile ./key.pem \
  --ssl-certfile ./cert.pem
```

### 2. Servidor Proxy

Ingresamos al directorio `app/` e iniciamos el servidor proxy:

```bash
cd app/
uvicorn main:app --reload
```

---

## ▶️ Uso

Una vez obtenidos los endpoints y reemplazados los dominios en las URLs hardcodeadas, recompilamos y renombramos cada app para instalarlas:

```bash
# Renombrar
mv base.apk       plataforma.apk
mv sad.apk        proydist.apk
mv inspeccion.apk inspeccion.apk
```

**Firma de APKs** (Android rechaza APKs sin firma):

```bash
java -jar uber-apk-signer.jar --apks *.apk
```

**Instalación:**

```bash
adb install plataforma.apk
adb install proydist.apk
adb install inspeccion.apk
```

Con estas apps apuntando al proxy, recolectamos la información necesaria para construir el servidor FastAPI que:

1. Define los **prefijos** y **endpoints finales**.
2. Captura **payload** y **metadatos** que pasan por el proxy.
3. Usa el **LLM con un pre-prompt** para devolver datos estructurados.
4. Analiza las imágenes que llegan en segundo plano.
5. Envía los resultados tanto al **servidor de destino** como al **usuario** que abrió el catastro.

---

## 📊 Características

| Característica | Android | Proxy IA |
|---|---|---|
| Captura de catastro | ✅ | — |
| Envío de imágenes al servidor | ✅ | ✅ |
| Procesamiento con Gemini IA | ❌ | 🚧 En diseño |
| Automatización del catastro eléctrico | ❌ | 🚧 En diseño |
| API intermediaria con FastAPI | — | ✅ |
| Cambio de servidor desde la aplicación | ✅ | — |
| Extracción de información de imágenes | ❌ | 🚧 En diseño |
| Funcionamiento sin conexión | ❌ | ❌ |
| Procesamiento de IA completamente local | ❌ | ❌ |
| Aplicación nativa independiente | ❌ | ❌ |

**Leyenda:** ✅ Implementado · 🚧 En diseño · ❌ No soportado · — No aplica

---

## 🧩 Conclusión

El proyecto permitió comprender el ecosistema de aplicaciones móviles involucradas en el catastro eléctrico, identificar sus flujos de autenticación, endpoints y esquemas de subida de fotografías, y redirigir el tráfico hacia un servidor intermedio bajo nuestro control.

La integración con un LLM  para el análisis automático de imágenes **está en fase de diseño**. Los endpoints definitivos del proxy, el esquema de metadatos y el flujo de reenvío al servidor de destino **aún no están cerrados** y se documentarán en próximas iteraciones.

**Próximos pasos:**

1. Definir el contrato final del endpoint `/cadastre/analizar`.
2. Implementar el pre-prompt y la validación de la respuesta JSON.
3. Persistir resultados con auditoría (hash, usuario, timestamp).
4. Reenviar el estado actualizado al servidor de destino.
5. Añadir revisión humana para casos de baja confianza.
6. Documentar el despliegue completo con Docker.
