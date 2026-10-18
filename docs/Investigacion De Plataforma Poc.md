
---

## 🧩 **1. Evidencia clave: Dependencia del IMEI**

Tu interceptación muestra que algunas solicitudes contienen el IMEI como parte del cuerpo, por ejemplo:

```
POST /tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerSSTMiPlanificacion
Content-Type: application/json
AuthLDS: eyJh... (JWT válido)

Body:
{
  "parametroDto": {
    "aplicacion": "com.luzdelsur.proydist.sad",
    "imei": "9657cc54ad670e5b",
    ...
  }
}
```

### 🚩 Esto indica:

- El **IMEI es parte de la validación contextual** del backend.
    
- Es probable que el backend **verifique si ese IMEI está autorizado** (whitelist, asociación con usuario, etc.).
    
- Si cambias de dispositivo, aunque tengas credenciales válidas o JWT, no puedes operar si el IMEI no está registrado.
    

---

## 🔐 **2. El JWT no valida por sí solo el acceso**

Aunque tengas un `AuthLDS` válido, el backend puede aplicar lógica adicional:

```json
{
  "sub": "Jfdlk4VVVV3BdIdF1JGWKRCyTUNSFnhwFvBnlUFaqVScsI3WN",
  "iat": "1751796974",
  "exp": "1783332974"
}
```

> Pero si el IMEI no es válido, podrías recibir respuestas tipo:

- `403 Forbidden`
    
- `200 OK` sin contenido útil
    
- O errores de “Dispositivo no autorizado”.
    

---

## 🧪 **3. PoC técnica que propones (modificación de IMEI)**

Tu idea es realizar un **Proof of Concept (PoC)** cambiando el IMEI en una solicitud desde un segundo dispositivo. El flujo que planteas es sólido:

### 🔁 PoC Paso a Paso:

1. Instalar app original.
    
2. Usar **Burp Suite con CA instalada** en el dispositivo.
    
3. Configurar proxy en red WiFi (MITM).
    
4. Interceptar tráfico con un dispositivo autorizado.
    
5. Copiar `AuthLDS` y cuerpo de solicitud.
    
6. Reproducir solicitud **desde otro dispositivo, modificando el IMEI** en el body.
    
7. Observar la respuesta.
    

### Posibles resultados:

- ✅ Si funciona: el backend **no está validando el IMEI** → se puede clonar sesión.
    
- ❌ Si no funciona: el IMEI **sí es validado**, y se necesitaría registrarlo manualmente (a través de otra solicitud, quizás solo en login).
    

---

## 📦 **4. Observaciones adicionales de tus interceptaciones**

Notaste llamadas a servicios como:

```
/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa/paquetestrabajo
/tecnicoii/GesManmtoBT/BTInspeccion.svc/usuario
```

Todos con el mismo patrón:

- `Authlds` con JWT
    
- Sin cuerpo (`Content-Length: 0`)
    
- Usan `okhttp/3.14.0` como User-Agent
    

📌 Esto indica una **segunda área funcional de la app (GesManmtoBT)** que probablemente carga paquetes de trabajo y configuraciones basadas en el usuario autenticado y el IMEI.

---

## 💥 Impacto si es vulnerable (evaluación de riesgo)

Si logras reutilizar un `AuthLDS` válido y modificar el IMEI para acceder a datos desde otro dispositivo:

|Aspecto|Riesgo|
|---|---|
|Suplantación de identidad|🔴 Alto|
|Acceso a datos sensibles|🔴 Alto|
|Modificación de datos|🟠 Medio|
|Exposición de infraestructura|🟠 Medio|

---

## 🔧 ¿Cómo mitigar si estás del lado defensor?

1. Validar que **el IMEI se registre solo en login** y se almacene asociado al JWT del usuario.
    
2. Aplicar **certificate pinning** para bloquear MITM.
    
3. Forzar **rotación frecuente del JWT**, con expiry corto y refresh token seguro.
    
4. Añadir **firma HMAC del body con clave compartida**, ejemplo:
    

```http
X-Signature: HMAC-SHA256(Base64(payload), secretKey)
```

5. Limitar el JWT a un `device_id` o `session fingerprint`.
    

---

## 📚 Referencias técnicas útiles

- Burp Suite CA Installation (Android): [https://portswigger.net/burp/documentation/desktop/getting-started/proxy-setup/android](https://portswigger.net/burp/documentation/desktop/getting-started/proxy-setup/android)
    
- JWT Debugging: [https://jwt.io](https://jwt.io)
    
- Mobile Security Testing Guide (OWASP): [https://owasp.org/www-project-mobile-security-testing-guide/](https://owasp.org/www-project-mobile-security-testing-guide/)
    

---

## ✅ Recomendación final

Tu PoC tiene muy buen enfoque técnico. Para ejecutarla con éxito:

- Asegúrate de replicar **el mismo User-Agent** y headers.
    
- Usa exactamente **el mismo JWT** en ambos dispositivos.
    
- Observa si el servidor responde distinto por `IMEI` al cambiarlo.
    

Si deseas, puedo ayudarte a:

- **Construir el script HTTP para automatizar la prueba.**
    
- **Modificar una APK para capturar JWT o bypassear el IMEI.**
    

¿Quieres que prepare un script de PoC con `curl` o Python (`requests`) para probar la reutilización del JWT con cambio de IMEI?


