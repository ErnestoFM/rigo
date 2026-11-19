;================================================================================
; ARCHIVO DESENSAMBLADO EJECUTABLE: Error en ALU: División Entre Cero en Instrucción de Máquina
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
0x2000:  DB  a          = 50      ; VARIABLE (int)
0x2004:  DB  t1         = 0       ; TEMPORAL (int)
0x3000:  DB  result     = 0       ; RESULTADO (int)

; --- SEGMENTO DE CÓDIGO (.CODE) ---
0x1000: LOAD   R1, 0x2000        # Carguen el valor de a en R1
0x1004: DIV    R1, #0            # Dividan entre el valor de 0 al registro R1
0x1008: STORE  0x3000, R1        # Almacenen el resultado en result
0x100C: HALT                     # Fin de ejecución
