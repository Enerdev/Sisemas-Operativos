# Taller de Políticas de Planificación de Procesos

**Curso:** Sistemas Operativos — 2026-II
**Universidad:** Universidad Nacional del Altiplano – Puno · Escuela Profesional de Ingeniería de Sistemas
**Estudiante:** Emerson Aldair Flores Flores · **Código:** 240439 · **Semestre:** 5.º

Simulador en Python de las políticas de planificación de CPU usadas en el taller:
FCFS, SJF (no expulsivo), SRTF (SJF expulsivo), Round Robin con cuanto `q` y
Prioridades sin desalojo. Calcula el diagrama de Gantt, los tiempos de retorno
y espera de cada proceso, sus medias y la varianza de la espera.

## Estructura

```
.
├── planificador.py   # algoritmos + métricas; imprime la solución de todos los ejercicios
├── graficos.py       # genera los diagramas de Gantt en PNG (carpeta gantt/)
├── resultados.txt    # salida completa de planificador.py
└── gantt/            # ej1.png, ej2.png, ej3.png, ej5.png, ej6.png, ej7.png
```

## Uso

```bash
python3 planificador.py            # imprime Gantt + tablas de cada ejercicio
python3 planificador.py > resultados.txt

pip install matplotlib
python3 graficos.py                # crea gantt/*.png
```

Para simular otra carga, crea la lista de procesos `(nombre, llegada, ráfaga[, prioridad])`:

```python
from planificador import crear, round_robin, reporte
procs = crear([("A", 0, 4), ("B", 2, 3), ("C", 4, 1)])
reporte("RR q=2", procs, round_robin(procs, 2))
```

## Convenciones

- Retorno = fin − llegada · Espera = retorno − ráfaga · Varianza poblacional (÷ n).
- Empates en SJF/SRTF/Prioridad: primero el que llegó antes; luego orden FIFO.
- Round Robin: un proceso que llega en el mismo instante en que otro agota su
  cuanto entra a la cola antes que el expulsado.
- Cambio de contexto despreciable.

## Resumen de resultados (espera media)

| Ejercicio | FCFS | SJF | SRTF | RR | Prioridad |
|-----------|------|-----|------|----|-----------|
| 1 | 4,25 | 4,00 | **2,75** | 5,25 (q=2) | – |
| 2 | 6,00 | **4,20** | – | 7,00 (q=1) · 6,20 (q=3) | – |
| 3 | 2,20 | **1,60** | **1,60** | 3,20 (q=4) | – |
| 5 | 4,25 | 4,00 | **2,75** | 5,25 (q=2) · 4,00 (q=3) | – |
| 6 | 8,40 | **6,00** | – | 11,00 (q=2) | – |
| 7 | 9,60 | **3,20** | – | 5,40 (q=1) | 8,20 |

El ejercicio 4 es teórico y está resuelto en el informe.
