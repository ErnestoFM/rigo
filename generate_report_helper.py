"""
================================================================================
ACTIVIDAD 1: DEFINICIÓN DE TOKENS Y EXPRESIONES REGULARES (ANALIZADOR LÉXICO C)
MATERIA: Traductores de Lenguajes
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import sys
from io import StringIO
import main

def export_execution_log():
    buffer = StringIO()
    sys.stdout = buffer
    
    main.main()
    
    sys.stdout = sys.__stdout__
    output = buffer.getvalue()
    
    filename = "Salida_Ejecucion_Consola.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
        
    print(f"✔ Salida de ejecución guardada correctamente en '{filename}'. Lista para incluir en el reporte PDF.")

if __name__ == "__main__":
    export_execution_log()
