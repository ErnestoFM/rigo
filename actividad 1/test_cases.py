"""
================================================================================
ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

# ----------------------------------------------------------------------
# CASOS DE PRUEBA VÁLIDOS (Sintaxis Correcta)
# ----------------------------------------------------------------------

# 1. Declaraciones simples de variables (Tipos básicos solicitados por el profesor)
TEST_VALID_SIMPLE_VARS = """// Caso 1: Declaraciones simples de variables
entero x;
flotante y;
booleano activo;
cadena nombre;
"""

# 2. Declaraciones de variables con inicialización
TEST_VALID_INITIALIZED_VARS = """// Caso 2: Declaraciones con inicialización
entero edad = 21;
flotante pi = 3.1416;
booleano bandera = verdadero;
cadena saludo = "Hola Compiladores";
"""

# 3. Declaraciones de constantes (Obligatoriamente inicializadas)
TEST_VALID_CONSTANTS = """// Caso 3: Declaraciones de constantes
constante entero LIMITE = 100;
const flotante GRAVEDAD = 9.80665;
constante cadena TITULO = "Analizador Sintactico";
"""

# 4. Uso de variables y constantes en expresiones aritméticas y lógicas
TEST_VALID_USAGE_EXPRESSIONS = """// Caso 4: Uso y sentencias de asignación
entero x = 10;
entero y = 20;
entero resultado;
resultado = (x + y) * 2;
activo = (x < y) && verdadero;
"""


# ----------------------------------------------------------------------
# CASOS DE PRUEBA INVÁLIDOS (Errores Sintácticos Requeridos en la Rúbrica)
# ----------------------------------------------------------------------

# 5. Identificadores Inválidos que inician con dígitos (Ejemplos de la práctica: entero 123x; cadena 123;)
TEST_INVALID_IDENTIFIERS = """// Caso 5: Identificadores inválidos (inician con números)
entero 123x;
cadena 123;
"""

# 6. Tipos de datos no válidos (Ejemplos de tipos fuera de entero, flotante, booleano, cadena)
TEST_INVALID_TYPES = """// Caso 6: Tipos no válidos
flotando y;
doble saldo;
"""

# 7. Omisión de punto y coma al final de declaraciones (booleano activo sin ;)
TEST_MISSING_SEMICOLONS = """// Caso 7: Falta de punto y coma al final
booleano activo
entero contador = 50
"""

# 8. Constante no inicializada (Constante sin asignación de valor inicial)
TEST_UNINITIALIZED_CONSTANT = """// Caso 8: Constante sin valor inicial
constante entero MAX;
const flotante PI_SIN_VALOR;
"""

# 9. Asignación mal formada o expresión rota
TEST_MALFORMED_ASSIGNMENT = """// Caso 9: Expresiones rotas o asignación incompleta
entero a = ;
x = y + ;
"""

# 10. Suite Integral Combinada con múltiples errores para demostrar recuperación sintáctica
TEST_COMBINED_ERRORS = """// Caso 10: Suite combinada con múltiples errores sintácticos
entero 123x;
flotando temperatura;
booleano flag
constante entero LIMITE_SIN_VALOR;
cadena 999;
total = ;
"""
