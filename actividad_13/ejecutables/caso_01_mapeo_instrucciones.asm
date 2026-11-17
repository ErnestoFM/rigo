;================================================================================
; ARCHIVO DESENSAMBLADO EJECUTABLE: Mapeo Directo y Asignación de Memoria Aritmética (Ejemplo Rúbrica)
; GENERADO POR: COMPILADOR ACTIVIDAD 13
; PROFESOR: RIGOBERTO CARDENAS LARIOS
;
; INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
; 1. DIAZ TORRES JAZMIN MONTSERRAT
; 2. FIERRO MELÉNDEZ ERNESTO HATUEY
; 3. HERNANDEZ GARCIA HECTOR GABRIEL
; 4. MILLAN GUERRERO OSWALDO JOSUE
;================================================================================

; --- CABECERA DE METADATOS ---
; MAGIC:        MVCO (0x4D56434F)
; ENTRY POINT:  0x1000
; ARCHITECTURE: 32-bit RISC Educational Processor

; --- SEGMENTO DE DATOS (.DATA) ---
0x2000:  DB  a          = 5       ; VARIABLE (int)
0x2004:  DB  b          = 10      ; VARIABLE (int)
0x2008:  DB  c          = 2       ; VARIABLE (int)
0x200C:  DB  t1         = 0       ; TEMPORAL (int)
0x2010:  DB  t2         = 0       ; TEMPORAL (int)
0x3000:  DB  result     = 0       ; RESULTADO (int)

; --- SEGMENTO DE CÓDIGO (.CODE) ---
0x1000: LOAD   R1, 0x2000        # Carguen el valor de a en R1
0x1004: ADD    R1, 0x2004        # Sumen el valor de b al registro R1
0x1008: MUL    R1, 0x2008        # Multipliquen por c a R1
0x100C: STORE  0x3000, R1        # Almacenen el resultado en result
0x1010: PRINT  0x3000            # Imprimir result
0x1014: HALT                     # Fin de ejecución
