"""
================================================================================
ACTIVIDAD 12: OPTIMIZACIÓN DE CÓDIGO INTERMEDIO
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
    Representa un caso de prueba para la verificación del optimizador de código intermedio.

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
    # CASOS VÁLIDOS (5) - OPTIMIZACIONES DE LA RÚBRICA
    # --------------------------------------------------------------------------
    TestCase(
        id_num=1,
        name="Análisis de Instrucciones Inalcanzables (Ejemplo Rúbrica)",
        category="Identificación de Código Muerto",
        is_valid=True,
        code="""
L1:
x = 10
goto L2
y = 20
L2:
z = x + y
result = z
""",
        expected_behavior="Elimina la instrucción 'y = 20' porque aparece inmediatamente tras 'goto L2' y antes de la etiqueta 'L2:'."
    ),

    TestCase(
        id_num=2,
        name="Análisis de Variables No Utilizadas (Ejemplo Rúbrica)",
        category="Identificación de Código Muerto",
        is_valid=True,
        code="""
a = 5
b = 10
c = b + 2
result = c
""",
        expected_behavior="Elimina la asignación 'a = 5' dado que la variable 'a' nunca se lee en ningún cálculo posterior."
    ),

    TestCase(
        id_num=3,
        name="Eliminación de Cálculos Repetidos / CSE (Ejemplo Rúbrica)",
        category="Eliminación de Instrucciones Redundantes",
        is_valid=True,
        code="""
t1 = a + b
t2 = a + b
result = t1
""",
        expected_behavior="Detecta que 'a + b' ya se encuentra computado en 't1' y elimina la instrucción redundante 't2 = a + b'."
    ),

    TestCase(
        id_num=4,
        name="Eliminación de Asignaciones Innecesarias / Sobrescritas (Ejemplo Rúbrica)",
        category="Eliminación de Instrucciones Redundantes",
        is_valid=True,
        code="""
temp = a
temp = b
result = temp
""",
        expected_behavior="Elimina 'temp = a' al ser sobrescrita inmediatamente por 'temp = b' y propaga la copia a 'result = b'."
    ),

    TestCase(
        id_num=5,
        name="Plegado y Propagación de Constantes (Ejemplo Rúbrica)",
        category="Pruebas y Validación de Optimización",
        is_valid=True,
        code="""
x = 10
t1 = x + 5
t2 = t1 + 10
result = t2
""",
        expected_behavior="Propaga la constante x=10 y pliega aritméticamente 10+5=15 y 15+10=25, produciendo 'result = 25'."
    ),

    # --------------------------------------------------------------------------
    # CASOS INVÁLIDOS / CASOS LÍMITE Y CONTROL DE ERRORES (5)
    # --------------------------------------------------------------------------
    TestCase(
        id_num=6,
        name="Salto hacia Etiqueta Inexistente en Código Intermedio",
        category="Control Semántico de Flujo",
        is_valid=False,
        code="""
x = 10
goto L_no_existe
result = x
""",
        expected_behavior="Detecta y reporta error semántico: salto incondicional a la etiqueta no definida 'L_no_existe'."
    ),

    TestCase(
        id_num=7,
        name="Uso de Variable No Inicializada en Expresión",
        category="Control Semántico de Variables",
        is_valid=False,
        code="""
result = variable_desconocida_xyz + 5
""",
        expected_behavior="Detecta y reporta error semántico: intento de operar con 'variable_desconocida_xyz' que nunca fue inicializada."
    ),

    TestCase(
        id_num=8,
        name="Instrucción TAC Mal Formada o Sintaxis Desconocida",
        category="Control Sintáctico de Código Intermedio",
        is_valid=False,
        code="""
= = + 5 10
""",
        expected_behavior="Detecta y reporta error de formato sintáctico en instrucción de código intermedio."
    ),

    TestCase(
        id_num=9,
        name="División por Cero Detectada en Optimización de Constantes",
        category="Control Aritmético en Compilación",
        is_valid=False,
        code="""
x = 100
t1 = x / 0
result = t1
""",
        expected_behavior="Detecta y reporta error aritmético: división entre cero en tiempo de compilación durante el plegado de constantes."
    ),

    TestCase(
        id_num=10,
        name="Salto Condicional con Operador Relacional Inválido",
        category="Control Sintáctico de Saltos Condicionales",
        is_valid=False,
        code="""
if a <> 10 goto L1
result = 10
L1:
result = 20
""",
        expected_behavior="Detecta operador relacional inválido '<>' en la condición del salto condicional."
    ),
]
