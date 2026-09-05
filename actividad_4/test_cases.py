"""
================================================================================
ACTIVIDAD 4: ANÁLISIS SINTÁCTICO DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

# =============================================================================
# CASOS DE PRUEBA VÁLIDOS (CONFORME A LA GUÍA Y CASOS AVANZADOS)
# =============================================================================

# Caso 1 (Oficial): Expresión aritmética simple con suma y multiplicación
TEST_VALID_ARITHMETIC_SIMPLE = "x + y * 5"

# Caso 2 (Oficial): Expresión aritmética con agrupación y división
TEST_VALID_ARITHMETIC_GROUPED = "(a - b) / c"

# Caso 3 (Oficial): Expresión lógica compuesta con operador relacional y conjunción
TEST_VALID_LOGIC_RELATIONAL = "10 > 5 && 3 <= 4"

# Caso 4 (Oficial): Expresión aritmética con múltiples agrupaciones multiplicadas
TEST_VALID_MULTIPLE_GROUPS = "(x + y) * (z - w)"

# Caso 5 (Extendido): Expresión lógica con disyunción y desigualdad
TEST_VALID_LOGIC_DISJUNCTION = "total >= 100 || descuento != 0"

# Caso 6 (Extendido): Expresión aritmética con igualdad relacional
TEST_VALID_FORMULA_EQUALITY = "(base * altura) / 2 == area"

# Caso 7 (Extendido): Expresión lógica combinada con paréntesis y disyunción
TEST_VALID_COMBINED_LOGIC = "(x > 0 && y > 0) || z == 100"

# Caso 8 (Extendido): Aritmética compleja con operaciones anidadas
TEST_VALID_COMPLEX_ARITHMETIC = "25 * (a + b) / (c - d) + 10"

# Caso 9 (Extendido): Aritmética con literales flotantes y relacionales
TEST_VALID_FLOAT_RELATIONAL = "precio * (1 - 0.15) <= presupuesto"

# Caso 10 (Extendido): Expresión lógica con operador de negación unario
TEST_VALID_UNARY_NOT = "!activo && (contador + 1 < limite)"


# =============================================================================
# CASOS DE PRUEBA INVÁLIDOS (GESTIÓN DE ERRORES SINTÁCTICOS REQUERIDOS)
# =============================================================================

# Caso 1 (Oficial): Operador aritmético sin término (operadores consecutivos '+ *')
TEST_INVALID_OP_WITHOUT_TERM = "x + * y"

# Caso 2 (Oficial): Comparación relacional sin expresión aritmética derecha
TEST_INVALID_COMPARISON_INCOMPLETE = "10 >"

# Caso 3 (Oficial): Paréntesis desbalanceados (falta paréntesis de cierre ')')
TEST_INVALID_UNBALANCED_OPEN_PAREN = "(a - b"

# Caso 4 (Oficial): Paréntesis desbalanceados y operador sin término dentro de agrupación
TEST_INVALID_OP_AND_PAREN_INCOMPLETE = "5 / (2 + )"

# Caso 5 (Extendido): Operador lógico al final sin término derecho
TEST_INVALID_LOGICAL_TRAILING = "10 > 5 &&"

# Caso 6 (Extendido): Operador lógico al inicio sin término izquierdo
TEST_INVALID_LOGICAL_LEADING = "&& 3 <= 4"

# Caso 7 (Extendido): Paréntesis desbalanceados por cierre sobrante
TEST_INVALID_UNBALANCED_EXTRA_CLOSE = "(x + y)) * 2"

# Caso 8 (Extendido): Falta de operador entre dos operandos adyacentes
TEST_INVALID_MISSING_OPERATOR = "a + b c"

# Caso 9 (Extendido): Operadores de comparación consecutivos inválidos
TEST_INVALID_CONSECUTIVE_COMPARISONS = "x == > y"

# Caso 10 (Extendido): Operador binario al inicio sin término izquierdo
TEST_INVALID_LEADING_BINARY_OP = "* 5 + 10"


# =============================================================================
# DICCIONARIO DE CASOS DE PRUEBA PARA INTERFAZ GRÁFICA Y AUTOMATIZACIÓN
# =============================================================================

ALL_TEST_CASES = {
    "Válidos": [
        ("Caso 1: Aritmética simple (x + y * 5) [Oficial]", TEST_VALID_ARITHMETIC_SIMPLE),
        ("Caso 2: Aritmética agrupada ((a - b) / c) [Oficial]", TEST_VALID_ARITHMETIC_GROUPED),
        ("Caso 3: Expresión lógica relacional (10 > 5 && 3 <= 4) [Oficial]", TEST_VALID_LOGIC_RELATIONAL),
        ("Caso 4: Agrupaciones multiplicadas ((x + y) * (z - w)) [Oficial]", TEST_VALID_MULTIPLE_GROUPS),
        ("Caso 5: Disyunción lógica (total >= 100 || descuento != 0)", TEST_VALID_LOGIC_DISJUNCTION),
        ("Caso 6: Fórmula con igualdad ((base * altura) / 2 == area)", TEST_VALID_FORMULA_EQUALITY),
        ("Caso 7: Lógica combinada anidada ((x > 0 && y > 0) || z == 100)", TEST_VALID_COMBINED_LOGIC),
        ("Caso 8: Aritmética compleja (25 * (a + b) / (c - d) + 10)", TEST_VALID_COMPLEX_ARITHMETIC),
        ("Caso 9: Expresión con flotantes (precio * (1 - 0.15) <= presupuesto)", TEST_VALID_FLOAT_RELATIONAL),
        ("Caso 10: Negación lógica unaria (!activo && (contador + 1 < limite))", TEST_VALID_UNARY_NOT),
    ],
    "Inválidos": [
        ("Caso 1: Operador sin término (x + * y) [Oficial]", TEST_INVALID_OP_WITHOUT_TERM),
        ("Caso 2: Comparación incompleta (10 >) [Oficial]", TEST_INVALID_COMPARISON_INCOMPLETE),
        ("Caso 3: Paréntesis desbalanceados ((a - b) [Oficial]", TEST_INVALID_UNBALANCED_OPEN_PAREN),
        ("Caso 4: Operador sin término en paréntesis (5 / (2 + )) [Oficial]", TEST_INVALID_OP_AND_PAREN_INCOMPLETE),
        ("Caso 5: Operador lógico sin término derecho (10 > 5 &&)", TEST_INVALID_LOGICAL_TRAILING),
        ("Caso 6: Operador lógico al inicio (&& 3 <= 4)", TEST_INVALID_LOGICAL_LEADING),
        ("Caso 7: Paréntesis de cierre sobrante ((x + y)) * 2)", TEST_INVALID_UNBALANCED_EXTRA_CLOSE),
        ("Caso 8: Falta operador entre términos (a + b c)", TEST_INVALID_MISSING_OPERATOR),
        ("Caso 9: Operadores de comparación consecutivos (x == > y)", TEST_INVALID_CONSECUTIVE_COMPARISONS),
        ("Caso 10: Operador binario al inicio (* 5 + 10)", TEST_INVALID_LEADING_BINARY_OP),
    ]
}
