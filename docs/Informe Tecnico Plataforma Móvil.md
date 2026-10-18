
## 📦 Nombre del paquete:

**`com.luzdelsur.plataforma.movil`**

## 🔍 Objeto de análisis:

Evaluar el funcionamiento del sistema de autenticación, intercambio de tokens JWT, y potenciales vectores de acceso o bypass de controles desde el dispositivo y la capa de red.

---

## 1. ⚙️ Estructura del Login (Java Decompilado)

### 🔹 Archivo clave:

**`LoginActivity.java`**

### 🔹 Elementos de autenticación:

```java
CredencialesDto credencialesDto = new CredencialesDto(
    DatosPersistentes.Session.getDominio(context),
    username,
    password,
    DatosPersistentes.Session.getEmpresa(context),
    DatosPersistentes.Session.getEmpresaContratante(context),
    UtilPlatafoma.getDeviceImei(context)
);
```

### 🧩 Parámetros enviados:

- `dominio`
    
- `usuario`
    
- `clave`
    
- `empresa`
    
- `empresaContratante`
    
- `imei` ← **elemento sensible usado como binding al dispositivo físico**
    

> 🔐 **Punto crítico:** El IMEI está siendo enviado **en crudo** y se usa para validar el dispositivo. Esta validación puede ser el factor principal por el cual no se puede acceder desde otros dispositivos.

---

## 2. 🔐 Sistema de Autenticación (JWT)

### 🔹 Estructura típica del token:

```http
AuthLDS: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

- **Algoritmo:** RS256
    
- **Payload decodificado:**
    
    ```json
    {
      "sub": "Identificador del usuario",
      "iat": "timestamp",
      "exp": "timestamp de expiración"
    }
    ```
    

### 🔹 Headers observados:

- `AuthLDS` → se usa en lugar de `Authorization` estándar
    
- Algunos endpoints usan `Authlds` (case sensitivity puede importar)
    

> 📌 _Posible diferencia entre módulos de la app:_

- `tecnicoi/` usa `AuthLDS`
    
- `tecnicoii/` usa `Authlds`
    

---

## 3. 📡 Estructura de Peticiones HTTP interceptadas

### Ejemplo relevante:

```http
POST /tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerSSTMiPlanificacion HTTP/1.1
AuthLDS: eyJh...
Content-Type: application/json

{
  "parametroDto": {
    "aplicacion": "com.luzdelsur.proydist.sad",
    "imei": "9657cc54ad670e5b",
    "porcentajeAvanceCero": false,
    "tipoAtencion": "SACATASTRO"
  }
}
```

> 💣 **Ataque sugerido (PoC):**

- Cambiar el `imei` en tiempo real usando Burp o proxy local para validar si el sistema realmente **verifica el IMEI** o simplemente lo **asocia al token generado**.
    

---

## 4. 🧠 Flujo persistente de datos internos

### Clase: `DatosPersistentes.Session`

Este módulo actúa como una **capa de SharedPreferences** y mantiene valores como:

- `empresa`
    
- `empresaContratante`
    
- `dominio`
    
- `usuario`
    
- `token JWT`
    
- `última sesión`
    

> 🧬 **Exfiltración posible:** Se puede inyectar código en Smali o modificar el APK para:

- Obtener los valores de la sesión en tiempo real
    
- Volcarlos a logs o archivos locales
    
- Inyectar `Toast.makeText()` con valores de sesión en ejecución
    

---

## 5. 💡 Vectores clave para ataque / bypass

|Técnica|Posibilidad|Requiere Root|Comentario|
|---|---|---|---|
|Modificación de `imei` en APK|Alta|No|Se puede forzar retorno falso en `UtilPlatafoma.getDeviceImei()`|
|Burp Suite + proxy + cert pinning bypass|Media|No|Solo si no hay SSL pinning fuerte o si se logra parcheo|
|Interceptar JWT con `adb logcat`|Media|No|Si el token se logea (no confirmado aún)|
|Hook con Frida a funciones de Java|Alta|Sí (o app debuggable)|Se puede interceptar `getDeviceImei`, `getToken`, etc.|
|Reutilizar token válido desde otro dispositivo|Baja-Media|No|Si el backend **no** valida el `imei`, podría usarse el token desde otros equipos|
|Patching de clases Java (APKTool)|Alta|No|Permite modificar comportamiento de validación interna|

---

## 6. 📁 Archivos sensibles del sistema (dispositivo rooteado)

- `/data/data/com.luzdelsur.plataforma.movil/shared_prefs/*.xml`  
    → Posiblemente almacene tokens, config, última sesión, empresa contratante.
    
- `/sdcard/Android/data/com.luzdelsur.plataforma.movil/`  
    → Posible caché, logs o fotos.
    

---

## 7. 🔐 Posible mecanismo de bloqueo (anti-abuso)

- IMEI como método de _device-binding_
    
- JWT firmados con **RSA**, difícil falsificar sin clave privada
    
- Validación backend en cada request usando `imei` y `sub`
    

---

## 8. 📸 Otras rutas sensibles detectadas

|Endpoint|Descripción|
|---|---|
|`/tecnicoii/GesManmtoBT/BTInspeccion.svc/usuario`|Obtiene info del usuario autenticado|
|`/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa/paquetestrabajo`|Probable carga de tareas|
|`/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion/suministro`|Config de inspección|
|`/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerSSTMiPlanificacion`|Ruta sensible con `imei`|

---

## 🔧 Recomendaciones para prueba de concepto

### 📲 PoC para validar bypass por IMEI

1. Instala la app original en un segundo equipo
    
2. Configura Burp/ZAP como proxy + certificado
    
3. Realiza login en dispositivo 1
    
4. Copia token JWT y cabeceras
    
5. En dispositivo 2:
    
    - Usa misma app
        
    - Intercepta petición y reemplaza el IMEI con el del dispositivo 1
        
    - Usa mismo token
        
6. Valida si el servidor responde exitosamente
    

---

## 🧪 Alternativas si hay pinning fuerte

- Usar **Frida + Objection** para bypass dinámico del pinning
    
- Reempaquetar la APK parcheando funciones como:
    
    - `checkServerTrusted`
        
    - `getDefaultHostnameVerifier`
        
- Modificar `getDeviceImei()` para retornar IMEI estático deseado
    

---

## ✅ Conclusión

- La app usa una combinación de **JWT + verificación de IMEI** como mecanismo de autenticación y control de acceso.
    
- Las peticiones dependen del token, pero también del IMEI incluido en el body de forma explícita.
    
- Si el backend **no valida fuertemente el IMEI**, se podría reusar tokens válidos desde otro dispositivo (con prueba controlada).
    
- Existen múltiples vectores para extracción o bypass del JWT si se logra interceptar el tráfico o modificar la APK.
    

---

¿Deseas que elabore un PoC real paso a paso (por ejemplo, usando Frida, APKTool o Smali)? ¿O necesitas que redacte el informe anterior como PDF?