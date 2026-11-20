"""
================================================================================
ACTIVIDAD 8: ANÁLISIS SEMÁNTICO - VERIFICACIÓN DE EXPRESIONES ARITMÉTICAS Y LÓGICAS
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


class TestCase:
    """
    Representa un caso de prueba para la verificación semántica de expresiones.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        id_num: int,
        name: str,
        category: str,
        is_valid: bool,
        code: str,
        expected_behavior: str
    ):
        self.id_num = id_num
        self.name = name
        self.category = category
        self.is_valid = is_valid
        self.code = code.strip()
        self.expected_behavior = expected_behavior


TEST_CASES: List[TestCase] = [
    # --------------------------------------------------------------------------
    # CASOS VÁLIDOS (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=1,
        name="Operaciones Aritméticas Enteras Válidas",
        category="Aritmética Homogénea (Rúbrica)",
        is_valid=True,
        code="""
int a = 10, b = 5;
int resultado = a + b;
int suma = 5 + 3;
""",
        expected_behavior="Validación exitosa de expresiones aritméticas entre enteros; cálculo evaluado: resultado = 15, suma = 8."
    ),

    TestCase(
        id_num=2,
        name="Operadores Lógicos con Expresiones Booleanas Válidas",
        category="Lógica Booleana (Rúbrica)",
        is_valid=True,
        code="""
bool activo = true;
bool inactivo = false;
bool resultado = activo && inactivo;
bool evaluacion = (10 > 5) && (3 < 8);
""",
        expected_behavior="Validación de operadores lógicos '&&' con operandos estrictamente booleanos; resultado = false, evaluacion = true."
    ),

    TestCase(
        id_num=3,
        name="Comparaciones Relacionales Homogéneas Válidas",
        category="Comparaciones Relacionales (Rúbrica)",
        is_valid=True,
        code="""
bool esIgual = (5 == 5);
bool esMenor = (3.14 < 6.28);
bool cadenaIgual = ("Hola" == "Hola");
""",
        expected_behavior="Comparaciones válidas entre tipos homogéneos (entero-entero, float-float, string-string) produciendo bool."
    ),

    TestCase(
        id_num=4,
        name="Expresión Aritmética Compleja con Precedencia de Operadores",
        category="Expresiones Complejas (Rúbrica)",
        is_valid=True,
        code="""
int resultadoComplejo = (10 + 20) * (30 - 15);
""",
        expected_behavior="Evaluación correcta de precedencia con paréntesis; cálculo evaluado: (30) * (15) = 450."
    ),

    TestCase(
        id_num=5,
        name="Conversión Explícita de Tipo (static_cast y Cast-C) Válida",
        category="Conversiones de Tipo (Rúbrica)",
        is_valid=True,
        code="""
int entero = 10;
float flotante = static_cast<float>(entero);
float resF = flotante + 2.5;
""",
        expected_behavior="Conversión explícita válida de entero a flotante sin pérdida y suma posterior con literal flotante (12.5)."
    ),

    # --------------------------------------------------------------------------
    # CASOS INVÁLIDOS CON GESTIÓN DE ERRORES (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=6,
        name="Error Aritmético: Operación Matemática con Cadena de Texto",
        category="Incompatibilidad Aritmética (Rúbrica)",
        is_valid=False,
        code="""
int edad = 25;
string nombre = "Juan";
int resultado = edad + nombre;
""",
        expected_behavior="Detección de 'Operación Aritmética con Tipo No Numérico: no se puede sumar un número con una cadena'."
    ),

    TestCase(
        id_num=7,
        name="Error Lógico: Operador Lógico Aplicado a Valor No Booleano",
        category="Operando No Booleano en Lógica (Rúbrica)",
        is_valid=False,
        code="""
bool errorLogico = true && 1;
""",
        expected_behavior="Detección de 'Operador Lógico con Operando No Booleano: el operando '1' no es un valor booleano'."
    ),

    TestCase(
        id_num=8,
        name="Error Relacional: Comparación Incompatible entre Cadena y Número",
        category="Comparación Incompatible (Rúbrica)",
        is_valid=False,
        code="""
bool errorComp = ("5" == 5);
""",
        expected_behavior="Detección de 'Comparación entre Tipos Incompatibles: no se puede comparar una cadena con un número mediante '=='."
    ),

    TestCase(
        id_num=9,
        name="Error Aritmético Crítico: División por Cero en Compilación",
        category="División por Cero (Rúbrica)",
        is_valid=False,
        code="""
int errorDiv = 10 / 0;
""",
        expected_behavior="Detección de 'División por Cero en Tiempo de Compilación con el operador '/' en línea 1'."
    ),

    TestCase(
        id_num=10,
        name="Error Aritmético: Intento de Operar Aritméticamente con Booleano",
        category="Operación Aritmética Inválida con Booleano",
        is_valid=False,
        code="""
bool flag = true;
int errorBool = 10 + flag;
""",
        expected_behavior="Detección de 'Operación Aritmética con Tipo No Numérico: no se puede aplicar '+' con un valor booleano'."
    )
]
