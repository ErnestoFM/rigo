"""
================================================================================
ACTIVIDAD 1: DEFINICIÓN DE TOKENS Y EXPRESIONES REGULARES (ANALIZADOR LÉXICO C)
MATERIA: COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

# Caso de Prueba Válido 1: Programa C con Estructuras, Bucles, Cadenas y Punteros
C_VALID_TEST_1 = """/*
 * Programa de prueba 1: Calculadora de factorial y manejo de registros
 * Autor: Equipo Compiladores C
 */
#include <stdio.h>

struct Persona {
    char nombre[50];
    int edad;
    float salario;
};

// Función principal
int main() {
    int n = 5;
    long long factorial = 1;
    float pi = 3.14159f;
    char delimitador = '\\n';

    /* Bucle para calcular el factorial de n */
    for (int i = 1; i <= n; ++i) {
        factorial *= i;
    }

    if (factorial > 100 && pi != 0.0) {
        printf("Factorial de %d = %lld\\n", n, factorial);
    } else {
        printf("Error en el cálculo\\n");
    }

    return 0;
}
"""

# Caso de Prueba Válido 2: Operadores de Bits, Switch-Case, Caracteres y Notación Científica
C_VALID_TEST_2 = """// Programa de prueba 2: Operadores de bits y flotantes en notación científica

int procesar_datos(unsigned int mascara) {
    float valor_sensor = 1.25e-3;
    double limite = 9.99;
    
    mascara = mascara & 0xFF00;
    mascara = mascara >> 4;
    
    switch (mascara) {
        case 0x10:
            valor_sensor += 0.5f;
            break;
        default:
            valor_sensor -= 0.1f;
    }
    
    return (valor_sensor <= limite) ? 1 : 0;
}
"""

# Caso de Prueba Inválido: Demostración de Errores Léxicos
C_INVALID_TEST = """// Programa con errores léxicos intencionados para validación

int main() {
    int $variable_invalida = 10;
    char@ caracter_extrano = 'a';
    
    // Cadena sin cerrar antes del fin de línea
    char* texto = "Esta cadena no se ha cerrado adecuadamente;
    
    float #numero = 45.67;
    return 0;
}
"""
