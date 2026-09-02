"""
================================================================================
ACTIVIDAD 2: MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

# CASO 1: Código C Válido (Control)
C_VALID_TEST = """// Caso 1: Código C perfectamente válido
#include <stdio.h>

int main() {
    int contador = 10;
    float promedio = 9.5f;
    printf("El promedio es: %f\\n", promedio);
    return 0;
}
"""

# CASO 2: Caracteres No Reconocidos
C_TEST_UNRECOGNIZED_CHARS = """// Caso 2: Prueba de Caracteres No Reconocidos (@, $, #, ~, ¿, ñ)
int main() {
    int $precio = 50;
    char@ simbolo = 'X';
    float #tasa = 0.16;
    bool ~estado = false;
    printf("¿Prueba de caracteres español ñ?");
    return 0;
}
"""

# CASO 3: Identificadores Mal Formados
C_TEST_MALFORMED_IDENTIFIERS = """// Caso 3: Prueba de Identificadores Mal Formados
int main() {
    int 123contador = 0;
    float 8promedio_final = 10.0;
    double 99suma = 55.4;
    return 0;
}
"""

# CASO 4: Literales Numéricos Incorrectos
C_TEST_INCORRECT_NUMBERS = """// Caso 4: Prueba de Literales Numéricos Incorrectos
int main() {
    float pi_invalido = 3.14.15;
    int hex_error = 0x12G4;
    double expo_incompleto = 1.5e+;
    return 0;
}
"""

# CASO 5: Cadenas Mal Formadas / Sin Cerrar
C_TEST_UNCLOSED_STRINGS = """// Caso 5: Prueba de Cadenas Mal Formadas o Sin Cerrar
int main() {
    char* mensaje = "Esta es una cadena de texto sin comilla de cierre;
    printf("Fin del programa\\n");
    return 0;
}
"""

# CASO 6: Demostración Combinada de Todas las Categorías de Error Léxico
C_TEST_COMBINED_ERRORS = """// Caso 6: Programa C completo con fallas léxicas combinadas
int main() {
    int 123contador = 10;                     // Error: Identificador mal formado
    float precio_múltiple = 99.99.5;          // Error: Número con múltiples puntos flotantes
    int mascara_hex = 0x55ZZ;                  // Error: Hexadecimal con dígitos inválidos
    char$ token_simbolo = 'A';                 // Error: Carácter no reconocido '$'
    char* mensaje = "Cadena que nunca se cerró; // Error: Cadena mal formada sin comilla
    return 0;
}
"""
