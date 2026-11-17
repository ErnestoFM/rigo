;================================================================================
; ARCHIVO DESENSAMBLADO EJECUTABLE: Violación de Segmento: Salto a Dirección Fuera de Memoria
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
0x2000:  DB  a          = 10      ; VARIABLE (int)
0x2004:  DB  b          = 10      ; VARIABLE (int)
0x2008:  DB  t1         = 0       ; TEMPORAL (int)
0x3000:  DB  result     = 0       ; RESULTADO (int)

; --- SEGMENTO DE CÓDIGO (.CODE) ---
0x1000: LOAD   R1, 0x2000        # Carguen el valor de a en R1
0x1004: ADD    R1, 0x2004        # Sumen el valor de b al registro R1
0x1008: JMP    0x9999            # Salto incondicional a 0x9999
0x100C: LOAD   R1, 0x2008        # Carguen t1 en R1
0x1010: STORE  0x3000, R1        # Almacenen en result
0x1014: HALT                     # Fin de ejecución
