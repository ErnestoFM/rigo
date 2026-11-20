"""
================================================================================
ACTIVIDAD 10: GENERACIÓN DE CÓDIGO INTERMEDIO (TRES DIRECCIONES - TAC)
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
    Representa un caso de prueba para la generación de código intermedio.

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
        name="Asignación de Constantes a Variables (Ejemplo Rúbrica)",
        category="Variables y Constantes (Rúbrica)",
        is_valid=True,
        code="""
x = 5;
y = 10;
""",
        expected_behavior="Genera temporales t1 = 5, x = t1, t2 = 10, y = t2 con comentarios descriptivos."
    ),

    TestCase(
        id_num=2,
        name="Uso de Variables en Suma Simple (Ejemplo Rúbrica)",
        category="Uso de Variables (Rúbrica)",
        is_valid=True,
        code="""
z = x + y;
""",
        expected_behavior="Genera t1 = x + y y z = t1."
    ),

    TestCase(
        id_num=3,
        name="Expresión Aritmética con Agrupación (Ejemplo Rúbrica)",
        category="Expresiones Aritméticas (Rúbrica)",
        is_valid=True,
        code="""
result = a * (b + c);
""",
        expected_behavior="Genera t1 = b + c, t2 = a * t1, result = t2."
    ),

    TestCase(
        id_num=4,
        name="Expresiones Lógicas y Comparación (Ejemplo Rúbrica)",
        category="Expresiones Lógicas (Rúbrica)",
        is_valid=True,
        code="""
flag = (x > y) && (z < 10);
""",
        expected_behavior="Genera t1 = 10, t2 = x > y, t3 = z < t1, t4 = t2 && t3, flag = t4."
    ),

    TestCase(
        id_num=5,
        name="Expresiones Anidadas Complejas (Ejemplo Rúbrica)",
        category="Manejo de Expresiones Anidadas (Rúbrica)",
        is_valid=True,
        code="""
total = (a + b) * (c - d);
result = (x + y) / (z - w);
""",
        expected_behavior="Genera instrucciones temporales multinivel para sumas, restas, multiplicación y división con guardia."
    ),

    # --------------------------------------------------------------------------
    # CASOS INVÁLIDOS CON GESTIÓN DE ERRORES (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=6,
        name="Validación de División por Cero con Guarda (Ejemplo Rúbrica)",
        category="Detección de Errores en Operaciones (Rúbrica)",
        is_valid=True,  # Genera instrucción condicional de guarda
        code="""
result = a / b;
""",
        expected_behavior="Emite guardia 'if b == 0 then error \"Division by zero\"' antes de calcular la división en t1."
    ),

    TestCase(
        id_num=7,
        name="Error Semántico: Operación Inválida entre Entero y Cadena (Ejemplo Rúbrica)",
        category="Validación de Tipos (Rúbrica)",
        is_valid=False,
        code="""
total = a + "string";
""",
        expected_behavior="Emite 'if type(a) != integer or type(\"string\") != integer then error \"Type mismatch\"' y bloquea la operación."
    ),

    TestCase(
        id_num=8,
        name="Error Crítico: División Explícita por Cero Constante",
        category="Error de División por Cero",
        is_valid=False,
        code="""
result = 100 / 0;
""",
        expected_behavior="Detecta división constante entre cero en compilación, emite guardia de error y reporta la anomalía."
    ),

    TestCase(
        id_num=9,
        name="Error Semántico: Operación Lógica con Operando de Texto",
        category="Error de Operando Lógico Inválido",
        is_valid=False,
        code="""
flag = (x > y) && "invalido";
""",
        expected_behavior="Emite guardia de verificación booleana y reporta que '&&' no admite cadenas de texto."
    ),

    TestCase(
        id_num=10,
        name="Error de Tipo: Asignación Incompatible de Cadena a Variable Entera",
        category="Error de Asignación Incompatible",
        is_valid=False,
        code="""
int contador = 10;
contador = "texto";
""",
        expected_behavior="Detecta incompatibilidad de tipos entre 'int' y 'string', emitiendo diagnóstico de error semántico."
    )
]
