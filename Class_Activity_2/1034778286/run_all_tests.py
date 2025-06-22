import traceback, importlib
from matplotlib import pyplot as plt
from Test.registry import TESTS
from Test.utils.report import generate_pdf_report

def main():
    results = []   # [(nombre, True/False, msg)]
    for name, func in TESTS:
        try:
            print(f"▶️  Ejecutando: {name}")
            func()                     # corre el test
            results.append((name, True,  "OK"))
            print("   ✅ PASÓ\n")
        except Exception as e:
            tb = traceback.format_exc()
            results.append((name, False, tb))
            print("   ❌ FALLO\n")

    # --- estadística ---
    passed  = sum(1 for _, ok, _ in results if ok)
    failed  = len(results) - passed

    # --- gráfico ---
    plt.figure(figsize=(4,4))
    plt.bar(["Pasaron", "Fallaron"], [passed, failed])
    plt.title("Resumen de tests")
    plt.ylabel("Cantidad")
    graph_path = "reports/tests_summary.png"
    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()
    print(f"📊 Gráfica guardada en {graph_path}")

    # --- PDF con detalle ---
    lines = [
        f"TOTAL: {len(results)}   ✅ {passed}   ❌ {failed}",
        "-------------------------------------------",
    ]
    for name, ok, msg in results:
        status = "OK" if ok else "FAIL"
        lines.append(f"[{status}] {name}")
        if not ok:
            lines.append("─ Detalle:")
            lines.extend(msg.splitlines()[:4])   # primeras líneas del stack-trace
            lines.append("")

    pdf_text = "\n".join(lines)
    generate_pdf_report("suite", pdf_text)

if __name__ == "__main__":
    import os, matplotlib
    os.makedirs("reports", exist_ok=True)
    main()
