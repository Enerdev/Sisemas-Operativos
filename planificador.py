#!/usr/bin/env python3
"""
Simulador de políticas de planificación de procesos
Curso: Sistemas Operativos 2026-II — UNA Puno
Autor: Emerson Aldair Flores Flores (240439)

Políticas: FCFS, SJF (no expulsivo), SRTF (SJF expulsivo),
           Round Robin (cuanto q), Prioridades no expulsivo.

Convenciones:
- Empates en SJF/SRTF/Prioridad: se desempata por tiempo de llegada y luego
  por orden de la lista (FIFO).
- Round Robin: si un proceso llega en el mismo instante en que otro agota su
  cuanto, el que llega entra a la cola ANTES que el expulsado.
- Retorno (turnaround) = fin - llegada ; Espera = retorno - ráfaga.
"""
from collections import deque


class Proceso:
    def __init__(self, nombre, llegada, rafaga, prioridad=0, orden=0):
        self.nombre = nombre
        self.llegada = llegada
        self.rafaga = rafaga
        self.prioridad = prioridad
        self.orden = orden


def _clave(p):
    return (p.llegada, p.orden)


def fcfs(procs):
    t, gantt = 0, []
    for p in sorted(procs, key=_clave):
        if t < p.llegada:
            gantt.append(("-", t, p.llegada))
            t = p.llegada
        gantt.append((p.nombre, t, t + p.rafaga))
        t += p.rafaga
    return gantt


def _no_expulsivo(procs, criterio):
    pend, t, gantt = sorted(procs, key=_clave), 0, []
    while pend:
        listos = [p for p in pend if p.llegada <= t]
        if not listos:
            sig = min(p.llegada for p in pend)
            gantt.append(("-", t, sig))
            t = sig
            continue
        p = min(listos, key=lambda x: (criterio(x), x.llegada, x.orden))
        gantt.append((p.nombre, t, t + p.rafaga))
        t += p.rafaga
        pend.remove(p)
    return gantt


def sjf(procs):
    return _no_expulsivo(procs, lambda p: p.rafaga)


def prioridad(procs):
    return _no_expulsivo(procs, lambda p: p.prioridad)


def srtf(procs):
    resto = {p.nombre: p.rafaga for p in procs}
    t, gantt = 0, []
    while any(resto.values()):
        listos = [p for p in procs if p.llegada <= t and resto[p.nombre] > 0]
        if not listos:
            actual = "-"
        else:
            actual = min(listos, key=lambda x: (resto[x.nombre], x.llegada, x.orden)).nombre
            resto[actual] -= 1
        if gantt and gantt[-1][0] == actual:
            gantt[-1] = (actual, gantt[-1][1], t + 1)
        else:
            gantt.append((actual, t, t + 1))
        t += 1
    return gantt


def round_robin(procs, q):
    pend = deque(sorted(procs, key=_clave))
    resto = {p.nombre: p.rafaga for p in procs}
    cola, t, gantt = deque(), 0, []

    def admitir(hasta):
        while pend and pend[0].llegada <= hasta:
            cola.append(pend.popleft())

    admitir(t)
    while cola or pend:
        if not cola:
            gantt.append(("-", t, pend[0].llegada))
            t = pend[0].llegada
            admitir(t)
            continue
        p = cola.popleft()
        uso = min(q, resto[p.nombre])
        gantt.append((p.nombre, t, t + uso))
        t += uso
        resto[p.nombre] -= uso
        admitir(t)                      # llegadas primero
        if resto[p.nombre] > 0:
            cola.append(p)              # luego el expulsado
    # fusionar tramos consecutivos del mismo proceso
    fus = []
    for n, a, b in gantt:
        if fus and fus[-1][0] == n and fus[-1][2] == a:
            fus[-1] = (n, fus[-1][1], b)
        else:
            fus.append((n, a, b))
    return fus


def metricas(procs, gantt):
    fin = {}
    for n, _, b in gantt:
        if n != "-":
            fin[n] = b
    filas = []
    for p in procs:
        ret = fin[p.nombre] - p.llegada
        filas.append((p.nombre, p.llegada, p.rafaga, fin[p.nombre], ret, ret - p.rafaga))
    n = len(filas)
    ret_m = sum(f[4] for f in filas) / n
    esp_m = sum(f[5] for f in filas) / n
    var = sum((f[5] - esp_m) ** 2 for f in filas) / n
    return filas, ret_m, esp_m, var


def gantt_texto(gantt):
    barra = "|" + "|".join(f" {n:^{max(1, (b - a) * 2 - 1)}} " for n, a, b in gantt) + "|"
    marcas, pos = "", 0
    for n, a, b in gantt:
        ancho = max(1, (b - a) * 2 - 1) + 3
        marcas += f"{a:<{ancho}}"
    marcas += str(gantt[-1][2])
    return barra + "\n" + marcas


def linea_tiempo(gantt):
    """Qué proceso ocupa la CPU en cada unidad de tiempo."""
    s = []
    for n, a, b in gantt:
        s += [n] * (b - a)
    return " ".join(s)


def reporte(titulo, procs, gantt):
    filas, ret_m, esp_m, var = metricas(procs, gantt)
    print(f"\n--- {titulo} ---")
    print(gantt_texto(gantt))
    print("CPU por unidad:", linea_tiempo(gantt))
    print(f"{'Proc':<5}{'Lleg':>5}{'Ráf':>5}{'Fin':>5}{'Ret':>5}{'Esp':>5}")
    for f in filas:
        print(f"{f[0]:<5}{f[1]:>5}{f[2]:>5}{f[3]:>5}{f[4]:>5}{f[5]:>5}")
    print(f"Retorno medio = {ret_m:.2f} | Espera media = {esp_m:.2f} | Varianza espera = {var:.2f}")
    return ret_m, esp_m, var


def crear(datos):
    return [Proceso(*d[:3], *(d[3:] or [0]), orden=i) for i, d in enumerate(datos)]


if __name__ == "__main__":
    ej1 = crear([("P0", 0, 6), ("P1", 1, 3), ("P2", 3, 2), ("P3", 5, 4)])
    ej2 = crear([("A", 0, 2), ("B", 0, 1), ("C", 0, 8), ("D", 0, 3), ("E", 0, 5)])
    ej3 = crear([("A", 0, 3), ("B", 1, 5), ("C", 3, 2), ("D", 9, 5), ("E", 12, 5)])
    ej6 = crear([("A", 0, 5), ("B", 0, 2), ("C", 0, 6), ("D", 0, 4), ("E", 0, 3)])
    ej7 = crear([("P1", 0, 10, 3), ("P2", 0, 1, 1), ("P3", 0, 2, 3), ("P4", 0, 1, 4), ("P5", 0, 5, 2)])

    casos = [
        ("EJERCICIO 1", ej1, [("FCFS", fcfs), ("SJF", sjf), ("SRTF", srtf), ("RR q=2", lambda p: round_robin(p, 2))]),
        ("EJERCICIO 2", ej2, [("FCFS", fcfs), ("SJF", sjf), ("RR q=1", lambda p: round_robin(p, 1)), ("RR q=3", lambda p: round_robin(p, 3))]),
        ("EJERCICIO 3", ej3, [("FCFS", fcfs), ("SJF", sjf), ("SRTF", srtf), ("RR q=4", lambda p: round_robin(p, 4))]),
        ("EJERCICIO 5", ej1, [("FCFS", fcfs), ("SJF", sjf), ("SRTF", srtf), ("RR q=2", lambda p: round_robin(p, 2)), ("RR q=3", lambda p: round_robin(p, 3))]),
        ("EJERCICIO 6", ej6, [("FCFS", fcfs), ("SJF", sjf), ("RR q=2", lambda p: round_robin(p, 2))]),
        ("EJERCICIO 7", ej7, [("FCFS", fcfs), ("SJF", sjf), ("Prioridad no expulsiva", prioridad), ("RR q=1", lambda p: round_robin(p, 1))]),
    ]
    for titulo, procs, politicas in casos:
        print("\n" + "=" * 60 + f"\n{titulo}\n" + "=" * 60)
        resumen = []
        for nombre, f in politicas:
            r = reporte(nombre, procs, f(procs))
            resumen.append((nombre, *r))
        print("\nResumen:")
        for n, r, e, v in resumen:
            print(f"  {n:<24} Ret={r:6.2f}  Esp={e:6.2f}  Var={v:6.2f}")
