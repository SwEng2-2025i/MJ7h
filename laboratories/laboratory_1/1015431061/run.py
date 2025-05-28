from app import create_app
from flask import Flask

app = create_app()

def list_routes():
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods}: {rule}")

# Configuración para mostrar rutas al iniciar
with app.app_context():
    list_routes()

if __name__ == '__main__':
    port = 5000
    print(f"\nStarting server on http://localhost:{port}")
    print("Press CTRL+C to quit\n")
    app.run(debug=True, port=port)