# Simulador del Barbero Dormilón

Simulador interactivo del problema del barbero dormilón, desarrollado como
herramienta educativa para el curso SIS 215 — Sistemas Operativos de la
Universidad Nacional del Altiplano.

## Contenido

- [`simulador_barbero_dormilon.html`](./simulador_barbero_dormilon.html):
  aplicación completa en un único archivo HTML, con estilos y JavaScript
  incluidos.

## Cómo usarlo

1. Descarga o clona este repositorio.
2. Abre `simulador_barbero_dormilon.html` en un navegador web moderno.
3. En la pantalla inicial, elige un caso, acepta las políticas de uso y entra
   al simulador.

No se necesita instalar dependencias ni iniciar un servidor. Las tipografías
personalizadas se obtienen de Google Fonts; si no hay conexión a Internet, el
simulador conserva fuentes alternativas del sistema.

## Funcionalidades

- Configuración de la cantidad de barberos, sillas de espera y clientes.
- Ajuste de los intervalos de llegada y duración de los cortes.
- Simulación paso a paso, en tiempo real o hasta completar la ejecución.
- Políticas de atención FIFO, SJF y prioridad, con opción de envejecimiento.
- Exclusión mutua configurable para observar una condición de carrera.
- Visualización del estado de los hilos, la memoria compartida, la bitácora de
  eventos y un diagrama de Gantt.
- Casos predeterminados, casos personalizados e historial de ejecuciones.
- Comparación de métricas, entre ellas clientes atendidos o rechazados, espera,
  utilización de los barberos y condiciones de carrera.
- Explicación teórica y ejemplos de solución en C con `pthreads`, Python con
  `threading` y pseudocódigo.
- Tema claro y oscuro.

## Alcance y privacidad

La simulación se ejecuta localmente en el navegador y utiliza clientes y
tiempos ficticios. Sus resultados sirven para estudiar el comportamiento del
algoritmo; no representan mediciones de rendimiento de un sistema operativo
real. El simulador no envía resultados a un servidor y guarda localmente la
preferencia de tema. Para más detalles, consulta la sección **Políticas** de la
aplicación.
