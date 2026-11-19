;================================================================================
; ARCHIVO DESENSAMBLADO EJECUTABLE: Bucle Iterativo WHILE con Acumulador y Salto Hacia Atrás
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
0x2000:  DB  contador   = 0       ; VARIABLE (int)
0x2004:  DB  limite     = 5       ; VARIABLE (int)
0x2008:  DB  acum       = 0       ; VARIABLE (int)
0x3000:  DB  result     = 0       ; RESULTADO (int)

; --- SEGMENTO DE CÓDIGO (.CODE) ---
0x1000: LOAD   R1, 0x2000        # Carguen contador para comparar
0x1004: CMP    R1, 0x2004        # Comparen R1 con limite
0x1008: JGE    0x1028            # Salto condicional a L_FIN
0x100C: LOAD   R1, 0x2008        # Carguen el valor de acum en R1
0x1010: ADD    R1, 0x2000        # Sumen el valor de contador al registro R1
0x1014: STORE  0x2008, R1        # Almacenen el resultado en acum
0x1018: LOAD   R1, 0x2000        # Carguen el valor de contador en R1
0x101C: ADD    R1, #1            # Sumen el valor de 1 al registro R1
0x1020: STORE  0x2000, R1        # Almacenen el resultado en contador
0x1024: JMP    0x1000            # Salto incondicional a L_INICIO
0x1028: LOAD   R1, 0x2008        # Carguen acum en R1
0x102C: STORE  0x3000, R1        # Almacenen en result
0x1030: PRINT  0x3000            # Imprimir result
0x1034: HALT                     # Fin de ejecución
