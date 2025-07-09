import sys
import os
import importlib.util
from datetime import datetime

# Agregar el directorio Test al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator, TestLogger

class TestSuite:
    """Suite de pruebas que ejecuta y consolida resultados"""
    
    def __init__(self):
        self.backend_logs = []
        self.frontend_logs = []
        self.backend_status = "FAILED"
        self.frontend_status = "FAILED"
        self.report_generator = ReportGenerator()
        
    def run_backend_tests(self):
        """Ejecuta las pruebas de backend y captura los resultados"""
        
        try:
            # Importar y ejecutar el módulo de pruebas backend
            from report_generator import TestLogger
            import sys
            import os
            
            # Importar BackEnd-Test
            backend_module_path = os.path.join(os.path.dirname(__file__), 'BackEnd-Test.py')
            spec = importlib.util.spec_from_file_location("BackEnd_Test", backend_module_path)
            backend_module = importlib.util.module_from_spec(spec)
            sys.modules["BackEnd_Test"] = backend_module
            spec.loader.exec_module(backend_module)
            
            # Crear logger para capturar salida
            logger = TestLogger()
            logger.start_capture()
            
            try:
                backend_module.integration_test()
                self.backend_status = "PASSED"
                print("Test Backend completadas exitosamente")
            except Exception as e:
                self.backend_status = "❌ FAILED"
                print(f"Test Backend fallaron: {str(e)}")
            finally:
                logger.stop_capture()
                self.backend_logs = logger.logs
                
        except ImportError as e:
            print(f"Error al importar pruebas Backend: {e}")
            self.backend_logs = [f"Error al importar: {str(e)}"]
            
    def run_frontend_tests(self):
        """Ejecuta las pruebas de frontend y captura los resultados"""
        
        try:
            # Importar y ejecutar el módulo de pruebas frontend
            frontend_module_path = os.path.join(os.path.dirname(__file__), 'FrontEnd-Test.py')
            spec = importlib.util.spec_from_file_location("FrontEnd_Test", frontend_module_path)
            frontend_module = importlib.util.module_from_spec(spec)
            sys.modules["FrontEnd_Test"] = frontend_module
            spec.loader.exec_module(frontend_module)
            
            # Crear logger para capturar salida
            logger = TestLogger()
            logger.start_capture()
            
            try:
                frontend_module.main()
                self.frontend_status = "PASSED"
                print("Test Frontend completadas exitosamente")
            except Exception as e:
                self.frontend_status = "FAILED"
                print(f"Test Frontend fallaron: {str(e)}")
            finally:
                logger.stop_capture()
                self.frontend_logs = logger.logs
                
        except ImportError as e:
            print(f"Error al importar pruebas Frontend: {e}")
            self.frontend_logs = [f"Error al importar: {str(e)}"]
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas en secuencia"""
        print("Iniciando Suite Completa de Pruebas")
        print("=" * 50)
        
        start_time = datetime.now()
        
        self.run_backend_tests()
        print("-" * 30)

        self.run_frontend_tests()
        print("-" * 30)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"Tiempo total de ejecución: {duration.total_seconds():.2f} seg")
        
        # Generar reporte consolidado
        print("Generando reporte consolidado...")
        report_file = self.report_generator.generate_consolidated_report(
            self.backend_logs,
            self.frontend_logs,
            self.backend_status,
            self.frontend_status
        )
        
        # Mostrar resumen final
        self.print_summary()
        
        return report_file
    
    def print_summary(self):
        """Imprime un resumen de los resultados"""
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 50)
        print(f"Backend:  {self.backend_status}")
        print(f"Frontend: {self.frontend_status}")
        print("-" * 50)
        
        overall_status = self._get_overall_status()
        print(f"Estado General: {overall_status}")
        print("=" * 50)
    
    def _get_overall_status(self):
        """Determina el estado general de todas las pruebas"""
        if "PASSED" in self.backend_status and "PASSED" in self.frontend_status:
            return "TODAS LAS PRUEBAS EXITOSAS"
        elif "FAILED" in self.backend_status and "FAILED" in self.frontend_status:
            return "TODAS LAS PRUEBAS FALLARON"
        else:
            return "PRUEBAS MIXTAS - RESULTADOS COMBINADOS"

def main():
    """Función principal del script"""
    print("Ejecutando todas las pruebas de integración...")
    
    suite = TestSuite()
    report_file = suite.run_all_tests()
    
    print(f"\n Reporte guardado en: {report_file}")

if __name__ == "__main__":
    main()
