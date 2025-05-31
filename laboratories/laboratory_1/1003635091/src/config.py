# Configuración de Swagger para Flasgger
SWAGGER_CONFIG = {
    # Cabeceras personalizadas (vacío por defecto)
    "headers": [],
    
    # Especificaciones (endpoints) de la documentación
    "specs": [
        {
            # Nombre del endpoint que servirá la especificación JSON
            "endpoint": 'apispec',
            
            # Ruta donde estará disponible la especificación
            "route": '/apispec.json'
        }
    ],
    
    # Ruta base para recursos estáticos (CSS, JS, etc.)
    "static_url_path": "/flasgger_static",
    
    # Habilitar la interfaz web de Swagger UI
    "swagger_ui": True,
    
    # Ruta donde se servirá la interfaz de usuario de Swagger
    "specs_route": "/apidocs/"
}