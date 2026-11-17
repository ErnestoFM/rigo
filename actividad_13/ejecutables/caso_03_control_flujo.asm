;================================================================================
; ARCHIVO DESENSAMBLADO EJECUTABLE: Estructura de Control IF-ELSE con Saltos Condicionales y Etiquetas
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
0x2000:  DB  a          = 25      ; VARIABLE (int)
0x2004:  DB  b          = 10      ; VARIABLE (int)
0x3000:  DB  result     = 0       ; RESULTADO (int)

; --- SEGMENTO DE CÓDIGO (.CODE) ---
0x1000: LOAD   R1, 0x2000        # Carguen a para comparar
0x1004: CMP    R1, 0x2004        # Comparen R1 con b
0x1008: JGT    0x1018            # Salto condicional a L1
0x100C: LOAD   R1, #0            # Carguen 0 en R1
0x1010: STORE  0x3000, R1        # Almacenen en result
0x1014: JMP    0x1020            # Salto incondicional a L2
0x1018: LOAD   R1, #1            # Carguen 1 en R1
0x101C: STORE  0x3000, R1        # Almacenen en result
0x1020: PRINT  0x3000            # Imprimir result
0x1024: HALT                     # Fin de ejecución
