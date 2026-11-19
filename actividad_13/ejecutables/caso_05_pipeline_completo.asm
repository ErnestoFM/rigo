;================================================================================
; ARCHIVO DESENSAMBLADO EJECUTABLE: Pipeline Completo de Extremo a Extremo desde Código Fuente
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
0x2000:  DB  a          = 14      ; VARIABLE (int)
0x2004:  DB  b          = 6       ; VARIABLE (int)
0x2008:  DB  t1         = 0       ; TEMPORAL (int)
0x200C:  DB  t2         = 0       ; TEMPORAL (int)
0x2010:  DB  t3         = 0       ; TEMPORAL (int)
0x3000:  DB  result     = 0       ; RESULTADO (int)

; --- SEGMENTO DE CÓDIGO (.CODE) ---
0x1000: LOAD   R1, #14           # Carguen 14 en R1
0x1004: STORE  0x2000, R1        # Almacenen en a
0x1008: LOAD   R1, #6            # Carguen 6 en R1
0x100C: STORE  0x2004, R1        # Almacenen en b
0x1010: LOAD   R1, #0            # Carguen 0 en R1
0x1014: STORE  0x3000, R1        # Almacenen en result
0x1018: LOAD   R1, 0x2000        # Carguen a para comparar
0x101C: CMP    R1, 0x2004        # Comparen R1 con b
0x1020: JGT    0x1028            # Salto condicional a L1
0x1024: JMP    0x103C            # Salto incondicional a L2
0x1028: LOAD   R1, 0x2000        # Carguen el valor de a en R1
0x102C: ADD    R1, 0x2004        # Sumen el valor de b al registro R1
0x1030: MUL    R1, #2            # Multipliquen por 2 a R1
0x1034: STORE  0x3000, R1        # Almacenen el resultado en result
0x1038: JMP    0x1048            # Salto incondicional a L3
0x103C: LOAD   R1, 0x2000        # Carguen el valor de a en R1
0x1040: SUB    R1, 0x2004        # Resten el valor de b al registro R1
0x1044: STORE  0x3000, R1        # Almacenen el resultado en result
0x1048: PRINT  0x3000            # Imprimir result
0x104C: HALT                     # Fin de ejecución
