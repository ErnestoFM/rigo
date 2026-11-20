"""
================================================================================
ACTIVIDAD 2: MANEJO Y GESTIÓN DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List


class TestCaseItem:
    """
    Representa un caso de prueba individual para el analizador léxico, con metadatos
    de regla evaluada, categoría y comportamiento esperado.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        id_num: int,
        title: str,
        category: str,
        code: str,
        is_valid: bool,
        rule_description: str,
        expected_behavior: str
    ):
        self.id_num = id_num
        self.title = title
        self.category = category
        self.code = code.strip()
        self.is_valid = is_valid
        self.rule_description = rule_description
        self.expected_behavior = expected_behavior


# ==============================================================================
# BANCO DE CASOS DE PRUEBA (VÁLIDOS E INVÁLIDOS - 100% RÚBRICA)
# ==============================================================================

# CASO 1: Código C Válido (Caso de Control sin errores)
C_VALID_TEST = """// Caso 1: Codigo C perfectamente valido (Caso de Control)
#include <stdio.h>

int main() {
    int contador = 10;
    float promedio = 9.5f;
    printf("El promedio es: %f\\n", promedio);
    return 0;
}"""

# CASO 2: Caracteres No Reconocidos
C_TEST_UNRECOGNIZED_CHARS = """// Caso 2: Prueba de Caracteres No Reconocidos fuera del alfabeto de C (@, $, ~, ¿, ñ)
int main() {
    int $precio = 50;
    char@ simbolo = 'X';
    bool ~estado = 0;
    printf("Prueba espanol con simbolo no ascii: ¿ y ñ");
    return 0;
}"""

# CASO 3: Identificadores Mal Formados
C_TEST_MALFORMED_IDENTIFIERS = """// Caso 3: Prueba de Identificadores Mal Formados (inician con digitos)
int main() {
    int 123contador = 0;
    float 8promedio_final = 10.0;
    double 99suma = 55.4;
    return 0;
}"""

# CASO 4: Literales Numéricos Incorrectos
C_TEST_INCORRECT_NUMBERS = """// Caso 4: Prueba de Literales Numericos Incorrectos (multiples puntos, hex invalido, expo trunco)
int main() {
    float pi_invalido = 3.14.15;
    int hex_error = 0x12G4;
    double expo_incompleto = 1.5e+;
    return 0;
}"""

# CASO 5: Cadenas Mal Formadas / Sin Cerrar
C_TEST_UNCLOSED_STRINGS = """// Caso 5: Prueba de Cadenas de Texto Mal Formadas (sin comilla de cierre antes del salto de linea)
int main() {
    char* mensaje = "Esta es una cadena de texto sin comilla de cierre;
    printf("Fin del programa\\n");
    return 0;
}"""

# CASO 6: Demostración Combinada de Todas las Categorías de Error Léxico
C_TEST_COMBINED_ERRORS = """// Caso 6: Programa C completo con fallas lexicas combinadas
int main() {
    int 123contador = 10;                     // Error: Identificador mal formado
    float precio_multiple = 99.99.5;          // Error: Numero con multiples puntos decimales
    int mascara_hex = 0x55ZZ;                  // Error: Hexadecimal con digitos no validos
    char$ token_simbolo = 'A';                 // Error: Caracter no reconocido '$'
    char* mensaje = "Cadena que nunca se cerro; // Error: Cadena mal formada sin comilla
    return 0;
}"""


TEST_1 = TestCaseItem(
    id_num=1,
    title="Código C Válido (Caso de Control)",
    category="CONTROL_VALIDO",
    code=C_VALID_TEST,
    is_valid=True,
    rule_description="Verificación de directivas de preprocesador, palabras clave, identificadores y literales estándar de C.",
    expected_behavior="Generación de 100% tokens válidos, 0 errores léxicos reportados y flujo limpio."
)

TEST_2 = TestCaseItem(
    id_num=2,
    title="Caracteres No Reconocidos en C",
    category="CARACTER_NO_RECONOCIDO",
    code=C_TEST_UNRECOGNIZED_CHARS,
    is_valid=False,
    rule_description="Detección y aislamiento de símbolos ajenos al juego de caracteres de C ($ , @ , ~ , ¿ , ñ).",
    expected_behavior="El manejador captura los caracteres no reconocidos indicando línea, columna y sugerencia de eliminación."
)

TEST_3 = TestCaseItem(
    id_num=3,
    title="Identificadores Mal Formados",
    category="IDENTIFICADOR_MAL_FORMADO",
    code=C_TEST_MALFORMED_IDENTIFIERS,
    is_valid=False,
    rule_description="Detección de identificadores que inician con números (violación de la regla [a-zA-Z_][a-zA-Z0-9_]*).",
    expected_behavior="Identificación de '123contador', '8promedio_final', '99suma' con sugerencia de renombrado válido."
)

TEST_4 = TestCaseItem(
    id_num=4,
    title="Literales Numéricos Incorrectos",
    category="NUMERO_INCORRECTO",
    code=C_TEST_INCORRECT_NUMBERS,
    is_valid=False,
    rule_description="Validación de constantes numéricas contra expresiones regulares de números flotantes, hex y científicos.",
    expected_behavior="Detección de '3.14.15' (múltiples puntos), '0x12G4' (hex inválido) y '1.5e+' (exponente incompleto)."
)

TEST_5 = TestCaseItem(
    id_num=5,
    title="Cadenas Mal Formadas Sin Delimitador",
    category="CADENA_MAL_FORMADA",
    code=C_TEST_UNCLOSED_STRINGS,
    is_valid=False,
    rule_description="Detección de literales de cadena que no se cierran antes del fin de línea o archivo.",
    expected_behavior="Aislamiento del lexema no terminado y emisión de advertencia de comilla faltante."
)

TEST_6 = TestCaseItem(
    id_num=6,
    title="Evaluación Combinada de Errores Léxicos",
    category="EVALUACION_INTEGRAL",
    code=C_TEST_COMBINED_ERRORS,
    is_valid=False,
    rule_description="Evaluación simultánea de las 4 categorías de errores en un solo módulo de código fuente C.",
    expected_behavior="Reporte exhaustivo y desglose estadístico de todas las incidencias encontradas en la misma corrida."
)

ALL_TEST_CASES = [TEST_1, TEST_2, TEST_3, TEST_4, TEST_5, TEST_6]
VALID_TEST_CASES = [t for t in ALL_TEST_CASES if t.is_valid]
INVALID_TEST_CASES = [t for t in ALL_TEST_CASES if not t.is_valid]
