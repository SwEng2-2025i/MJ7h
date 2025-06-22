import os
import pytest
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from Cleanup import cleanup_tasks, cleanup_users

# Directorio de reportes
REPORT_DIR = os.path.join(os.getcwd(), "reports")

@pytest.fixture(scope="session")
def driver():
    options = Options()
    # options.add_argument("--headless")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

@pytest.fixture(autouse=True)
def clean_db():
    cleanup_tasks()
    cleanup_users()
    yield
    cleanup_tasks()
    cleanup_users()


def pytest_collection_modifyitems(session, config, items):
    backend = [i for i in items if "backend" in i.nodeid]
    frontend = [i for i in items if "frontend" in i.nodeid]
    others = [i for i in items if i not in backend + frontend]
    items[:] = backend + frontend + others


def pytest_sessionstart(session):
    session.results = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.session.results.append({
            "name": item.nodeid,
            "outcome": rep.outcome.upper()
        })


def pytest_sessionfinish(session, exitstatus):
    os.makedirs(REPORT_DIR, exist_ok=True)
    existing = [f for f in os.listdir(REPORT_DIR) if f.startswith("report_") and f.endswith(".pdf")]
    seqs = [int(f.split("_")[1].split(".")[0]) for f in existing] if existing else []
    next_seq = max(seqs) + 1 if seqs else 1
    filename = os.path.join(REPORT_DIR, f"report_{next_seq:03}.pdf")

    total = len(session.results)
    passed = sum(1 for r in session.results if r["outcome"] == "PASSED")
    failed = sum(1 for r in session.results if r["outcome"] == "FAILED")

    # Configurar documento y estilos
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            title=f"Informe de Tests #{next_seq:03}")
    styles = getSampleStyleSheet()
    # Estilo compacto para celdas largas
    small_style = ParagraphStyle(
        'SmallBody', parent=styles['BodyText'], fontSize=8,
        leading=10, splitLongWords=True
    )
    story = []

    # Título principal
    story.append(Paragraph("<b>Aplicación de Tareas</b>", styles['Title']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"<b>Informe de Tests #{next_seq:03}</b>", styles['Heading1']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Total de pruebas: {total}  |  Pasadas: {passed}  |  Fallidas: {failed}", styles['Heading2']))
    story.append(Spacer(1, 18))

    def add_section(title, results):
        if not results:
            return
        # Descripción de la sección
        desc = {
            'Backend Tests': 'Pruebas de la API de backend: creación, verificación y eliminación de usuarios y tareas.',
            'Frontend Tests': 'Pruebas E2E de frontend: interacción vía UI con Selenium y comprobaciones en backend.'
        }.get(title, 'Otras pruebas.')

        story.append(Paragraph(f"<b>{title}</b>", styles['Heading2']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(desc, styles['Normal']))
        story.append(Spacer(1, 12))

        # Tabla detallada
        data = [["Caso", "Características", "Resultado"]]
        for idx, r in enumerate(results, start=1):
            cell = Paragraph(r['name'], small_style)
            data.append([str(idx), cell, r['outcome']])
        # Ajuste de anchos: más espacio para características
        table = Table(data, colWidths=[40, 380, 100])
        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (2,1), (2,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('WORDWRAP', (1,1), (1,-1), 'CJK')
        ])
        # Colorear resultados
        for i, r in enumerate(results, start=1):
            clr = colors.green if r['outcome'] == 'PASSED' else colors.red
            table_style.add('TEXTCOLOR', (2, i), (2, i), clr)
        table.setStyle(table_style)
        story.append(table)
        story.append(Spacer(1, 12))

        # Score de la sección
        sec_total = len(results)
        sec_passed = sum(1 for r in results if r['outcome'] == 'PASSED')
        score = round((sec_passed / sec_total) * 100) if sec_total else 0
        story.append(Paragraph(f"Score de sección: {score}% ({sec_passed}/{sec_total} tests)", styles['Normal']))
        story.append(Spacer(1, 24))

    # Dividir resultados
    backend = [r for r in session.results if 'backend' in r['name']]
    frontend = [r for r in session.results if 'frontend' in r['name']]
    others = [r for r in session.results if r not in backend + frontend]

    # Agregar secciones
    add_section("Backend Tests", backend)
    story.append(PageBreak())
    add_section("Frontend Tests", frontend)
    if others:
        story.append(PageBreak())
        add_section("Otros Tests", others)

    # Generar PDF
    doc.build(story)
    print(f"✅ PDF generado: {filename}")
