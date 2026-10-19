#!/usr/bin/env python3
"""
Genera los diagramas de Gantt (PNG) de todos los ejercicios del taller.
Uso:  python3 graficos.py      -> crea la carpeta gantt/ con un PNG por ejercicio
Requiere: matplotlib  (pip install matplotlib)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from planificador import (crear, fcfs, sjf, srtf, round_robin, prioridad, metricas)

COLORES = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2"]


def dibujar(titulo, procs, politicas, archivo):
    n = len(politicas)
    fig, ejes = plt.subplots(n, 1, figsize=(11, 1.0 + 1.25 * n * len(procs) / 4 + 0.6 * n))
    if n == 1:
        ejes = [ejes]
    nombres = [p.nombre for p in procs]
    color = {nm: COLORES[i % len(COLORES)] for i, nm in enumerate(nombres)}
    for ax, (etq, f) in zip(ejes, politicas):
        g = f(procs)
        _, ret_m, esp_m, _ = metricas(procs, g)
        fin = g[-1][2]
        for nm, a, b in g:
            if nm == "-":
                continue
            y = nombres.index(nm)
            ax.barh(y, b - a, left=a, color=color[nm], edgecolor="black", height=0.6)
            if b - a >= 1:
                ax.text((a + b) / 2, y, nm, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        for p in procs:  # marca de llegada
            ax.plot(p.llegada, nombres.index(p.nombre), marker="v", color="black", markersize=5)
        ax.set_yticks(range(len(nombres)))
        ax.set_yticklabels(nombres)
        ax.invert_yaxis()
        ax.set_xticks(range(0, fin + 1))
        ax.set_xlim(0, fin)
        ax.grid(axis="x", linestyle=":", alpha=0.6)
        ax.set_title(f"{etq}   |   retorno medio = {ret_m:.2f}   espera media = {esp_m:.2f}", fontsize=10, loc="left")
    ejes[-1].set_xlabel("Tiempo (unidades)   ▼ = instante de llegada")
    fig.suptitle(titulo, fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(archivo, dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs("gantt", exist_ok=True)
    ej1 = crear([("P0", 0, 6), ("P1", 1, 3), ("P2", 3, 2), ("P3", 5, 4)])
    ej2 = crear([("A", 0, 2), ("B", 0, 1), ("C", 0, 8), ("D", 0, 3), ("E", 0, 5)])
    ej3 = crear([("A", 0, 3), ("B", 1, 5), ("C", 3, 2), ("D", 9, 5), ("E", 12, 5)])
    ej6 = crear([("A", 0, 5), ("B", 0, 2), ("C", 0, 6), ("D", 0, 4), ("E", 0, 3)])
    ej7 = crear([("P1", 0, 10, 3), ("P2", 0, 1, 1), ("P3", 0, 2, 3), ("P4", 0, 1, 4), ("P5", 0, 5, 2)])
    rr = lambda q: (lambda p: round_robin(p, q))
    trabajos = [
        ("Ejercicio 1", ej1, [("a) FCFS", fcfs), ("b) SJF", sjf), ("c) SRTF", srtf), ("d) RR q=2", rr(2))], "ej1.png"),
        ("Ejercicio 2", ej2, [("a) FCFS", fcfs), ("b) SJF", sjf), ("c) RR q=1", rr(1)), ("d) RR q=3", rr(3))], "ej2.png"),
        ("Ejercicio 3", ej3, [("a) FCFS", fcfs), ("b) SJF", sjf), ("c) SRTF", srtf), ("d) RR q=4", rr(4))], "ej3.png"),
        ("Ejercicio 5", ej1, [("a) FCFS", fcfs), ("b) SJF", sjf), ("c) SRTF", srtf), ("d) RR q=2", rr(2)), ("e) RR q=3", rr(3))], "ej5.png"),
        ("Ejercicio 6", ej6, [("a) FCFS", fcfs), ("b) SJF", sjf), ("c) RR q=2", rr(2))], "ej6.png"),
        ("Ejercicio 7", ej7, [("FCFS", fcfs), ("SJF", sjf), ("Prioridad sin desalojo", prioridad), ("RR q=1", rr(1))], "ej7.png"),
    ]
    for t, p, pol, arch in trabajos:
        dibujar(t, p, pol, os.path.join("gantt", arch))
        print("generado", arch)
