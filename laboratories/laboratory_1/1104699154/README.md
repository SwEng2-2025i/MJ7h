# 🧪 **Multichannel Notification System (REST API)**

**Nombre completo:** Diego Humberto Lavado González \\
**Número de documento:** 1104699154  

---

## 📝 Descripción general

Este sistema permite registrar usuarios con múltiples canales de notificación (email, SMS, consola) y enviar mensajes utilizando el canal preferido. Si el canal falla, se utiliza un canal alternativo disponible mediante el patrón **Chain of Responsibility**.

Incluye documentación Swagger para explorar y probar los endpoints fácilmente desde el navegador.

---

## 🎯 Funcionalidades

- Registrar usuarios con canales de notificación preferidos y alternativos.
- Enviar notificaciones que se enrutan automáticamente a través de una cadena de canales.
- Registrar cada intento de notificación con un **logger Singleton**.
- API REST construida con Flask y documentada con Swagger.

---

## ⚙️ Endpoints REST

| Método | Ruta                     | Descripción                                |
|--------|--------------------------|--------------------------------------------|
| POST   | `/users`                 | Registrar un nuevo usuario                 |
| GET    | `/users`                 | Listar todos los usuarios                  |
| POST   | `/notifications/send`    | Enviar una notificación a un usuario       |

### Ejemplos de uso (curl)

Registrar usuario
```bash
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d "{\"name\":\"Juan\",\"preferred_channel\":\"email\",\"available_channels\":[\"email\",\"sms\",\"console\"]}"
```


Enviar notificación:

```
curl -X POST http://127.0.0.1:5000/notifications/send -H "Content-Type: application/json" -d "{\"user_name\":\"Juan\",\"message\":\"Tu cita es mañana\"}"
```

Ver usuarios:
```
curl http://127.0.0.1:5000/users
```
---

## ♻️ Patrones de diseño aplicados
1. **Chain of Responsibility**

Se usa para gestionar el intento de envío de notificaciones por múltiples canales. Cada canal intenta enviar el mensaje y, si falla, delega al siguiente en la cadena.
2. **Singleton**

El logger que registra los intentos de notificación está implementado como Singleton. Esto garantiza que todos los canales compartan la misma instancia y se eviten duplicaciones.

---
## 📊 Diagrama de clases (UML)

```mermaid 
```

---
## ▶️ Cómo ejecutar

1. Instala las dependencias:

```
pip install Flask flask-restful flasgger
```

2. Ejecuta el servidor:

```
python main.py
```

3. Abre tu navegador en:

```
http://127.0.0.1:5000/apidocs/

```
Para poder explorar la API con Swagger.

---
## 🗂️ Estructura del proyecto

```
laboratory_1/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── user.py
│   ├── channels/
│   │   ├── base_channel.py
│   │   ├── email.py
│   │   ├── sms.py
│   │   └── console.py
│   ├── routes/
│   │   ├── user_routes.py
│   │   └── notification_routes.py
│   └── utils/
│       └── logger.py
│
├── main.py
├── requirements.txt
└── README.md
```





