import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def pytest_sessionfinish(session, exitstatus):
    # Obtener el terminal reporter para estadísticas
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    passed = len(reporter.stats.get('passed', []))
    failed = len(reporter.stats.get('failed', []))
    total = passed + failed

    # Directorio para reportes
    folder = os.path.join(os.getcwd(), "test_reports")
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(folder, f"report_{timestamp}.pdf")

    # Generar PDF con gráfica y resumen
    with PdfPages(pdf_path) as pdf:
        # Página de gráfico
        fig1, ax = plt.subplots()
        ax.bar(['✅ Pasaron', '❌ Fallaron'], [passed, failed])
        ax.set_title('Resumen de pruebas')
        ax.set_ylabel('Número de tests')
        pdf.savefig(fig1)
        plt.close(fig1)

        # Página de texto
        fig2 = plt.figure(figsize=(8, 6))
        texto = (
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Total de pruebas: {total}\n"
            f"Pruebas que pasaron: {passed}\n"
            f"Pruebas que fallaron: {failed}\n"
        )
        fig2.text(0.1, 0.5, texto, fontsize=12, va='center')
        pdf.savefig(fig2)
        plt.close(fig2)

    print(f"\n📄 Reporte generado en: {pdf_path}")
