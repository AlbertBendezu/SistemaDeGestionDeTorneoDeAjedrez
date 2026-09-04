# Administrador de Torneos de Ajedrez (Round Robin)
El objetivo principal fue aplicar los pilares de la Programación Orientada a Objetos (POO) y resolver problemas lógicos específicos de la competencia, como el manejo de descansos (BYE) cuando hay participantes impares.

## Librerias 
*   **Python** como lenguaje principal.
*   **Pandas & Openpyxl** para la persistencia de datos en archivos de Excel (`.xlsx`).
*   **Numpy** para la estructuración y manipulación de los arreglos estadísticos.
*   **Matplotlib** para la generación de reportes visuales de rendimiento.

### Resolución del problema de jugadores impares
Para el fixture utilicé el algoritmo de rotación Round Robin. Cuando el torneo cuenta con un número impar de jugadores, el sistema inyecta automáticamente un objeto `Jugador` virtual llamado "BYE". 
Toda la lógica de registro de resultados está blindada para detectar al "BYE" y otorgar los puntos correspondientes al jugador real de manera automática sin romper la matriz de datos ni el historial de rondas.

### Encapsulamiento
Para proteger la integridad de los datos durante la ejecución, todos los atributos críticos de las clases (`Jugador`, `Partida`, `Torneo`) están definidos como privados (`__atributo`). El acceso y modificación de estos estados se realiza estrictamente a través de decoradores `@property`, evitando mutaciones accidentales desde módulos externos.

## Reportes
El módulo de estadísticas procesa los datos acumulados para mostrar:
*   Posiciones actuales en un gráfico de barras.
*   Proporción de victorias por participante (gráfico de pastel).
*   Línea de tiempo con la evolución de puntos ronda por ronda.
*   Comparativa de rendimiento (Victorias vs Empates vs Derrotas) por jugador.

## Uso

1. Instala las dependencias necesarias en la terminal o cmd:
   pip install pandas numpy matplotlib openpyxl
   
2. Ejecuta el archivo principal:
   python main.py
   
*(Nota: Al guardar el torneo se generarán los archivos `jugadores.xlsx` y `partidas.xlsx` en la raíz del proyecto para poder reanudarlo después).*
