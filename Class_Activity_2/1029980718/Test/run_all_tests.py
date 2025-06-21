#!/usr/bin/env python3
"""
Script principal para ejecutar todas las pruebas de integración
Ejecuta tanto las pruebas del BackEnd como del FrontEnd con limpieza de datos y generación de reportes
"""

import sys
import os
import time
from datetime import datetime

# Agregar el directorio Test al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import importlib.util
    
    # Cargar BackEnd-Test.py
    spec_backend = importlib.util.spec_from_file_location("BackEnd_Test", "BackEnd-Test.py")
    backend_module = importlib.util.module_from_spec(spec_backend)
    spec_backend.loader.exec_module(backend_module)
    BackEndIntegrationTest = backend_module.BackEndIntegrationTest
    
    # Cargar FrontEnd-Test.py
    spec_frontend = importlib.util.spec_from_file_location("FrontEnd_Test", "FrontEnd-Test.py")
    frontend_module = importlib.util.module_from_spec(spec_frontend)
    spec_frontend.loader.exec_module(frontend_module)
    FrontEndIntegrationTest = frontend_module.FrontEndIntegrationTest
    
except ImportError as e:
    print(f"❌ Error importando módulos de prueba: {e}")
    print("Asegúrate de que los archivos BackEnd-Test.py y FrontEnd-Test.py estén en el directorio Test/")
    sys.exit(1)

def print_separator(title):
    """Imprime un separador visual con título"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_services_running():
    """Verifica que los servicios estén ejecutándose"""
    import requests
    
    services = {
        "Users Service": "http://localhost:5001/users",
        "Tasks Service": "http://localhost:5002/tasks",
        "Frontend": "http://localhost:5000"
    }
    
    print("🔍 Verificando que los servicios estén ejecutándose...")
    
    for service_name, url in services.items():
        try:
            if service_name == "Frontend":
                response = requests.get(url, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            if response.status_code in [200, 404]:  # 404 es OK para endpoints que requieren ID
                print(f"✅ {service_name}: Ejecutándose")
            else:
                print(f"⚠️  {service_name}: Respuesta inesperada (código {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {service_name}: No disponible - {str(e)}")
            return False
    
    return True

def run_backend_tests():
    """Ejecuta las pruebas del BackEnd"""
    print_separator("PRUEBAS DE INTEGRACIÓN - BACKEND")
    
    try:
        backend_test = BackEndIntegrationTest()
        backend_test.run_integration_test()
        return True
    except Exception as e:
        print(f"❌ Error en las pruebas del BackEnd: {str(e)}")
        return False

def run_frontend_tests():
    """Ejecuta las pruebas del FrontEnd"""
    print_separator("PRUEBAS DE INTEGRACIÓN - FRONTEND")
    
    try:
        frontend_test = FrontEndIntegrationTest()
        frontend_test.run_integration_test()
        return True
    except Exception as e:
        print(f"❌ Error en las pruebas del FrontEnd: {str(e)}")
        return False

def main():
    """Función principal"""
    start_time = datetime.now()
    
    print_separator("INICIANDO SUITE DE PRUEBAS DE INTEGRACIÓN")
    print(f"🕐 Hora de inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar servicios
    if not check_services_running():
        print("\n❌ Algunos servicios no están disponibles.")
        print("Por favor, asegúrate de que estén ejecutándose:")
        print("  - Users Service: python Users_Service/main.py")
        print("  - Tasks Service: python Task_Service/main.py")
        print("  - Frontend: python Front-End/main.py")
        return False
    
    results = {
        'backend': False,
        'frontend': False
    }
    
    # Ejecutar pruebas del BackEnd
    print("\n⏳ Esperando 2 segundos antes de iniciar las pruebas...")
    time.sleep(2)
    results['backend'] = run_backend_tests()
    
    # Pausa entre pruebas
    print("\n⏳ Esperando 5 segundos antes de las pruebas del FrontEnd...")
    time.sleep(5)
    
    # Ejecutar pruebas del FrontEnd
    results['frontend'] = run_frontend_tests()
    
    # Resumen final
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_separator("RESUMEN DE EJECUCIÓN")
    print(f"🕐 Hora de inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🕐 Hora de fin: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Duración total: {duration}")
    print("\n📊 Resultados:")
    print(f"  BackEnd Tests: {'✅ PASSED' if results['backend'] else '❌ FAILED'}")
    print(f"  FrontEnd Tests: {'✅ PASSED' if results['frontend'] else '❌ FAILED'}")
    
    # Verificar reportes generados
    reports_dir = "Test/reports"
    if os.path.exists(reports_dir):
        reports = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]
        print(f"\n📄 Reportes PDF generados: {len(reports)}")
        for report in sorted(reports):
            print(f"  - {report}")
    
    success = all(results.values())
    if success:
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los reportes para más detalles.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 