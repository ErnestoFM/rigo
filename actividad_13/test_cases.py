"""
================================================================================
ACTIVIDAD 13: GENERACIÓN DE CÓDIGO - BANCO DE CASOS DE PRUEBA (VÁLIDOS E INVÁLIDOS)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Dict, Any, Optional


class TestCaseCodeGeneration:
    """
    Representa un caso de prueba para el generador de código, con soporte tanto
    para código intermedio directo (TAC) como para código fuente de alto nivel.

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
        code_input: str,
        is_source_code: bool,
        is_valid: bool,
        rule_description: str,
        expected_behavior: str,
        initial_data: Optional[Dict[str, int]] = None
    ):
        self.id_num = id_num
        self.title = title
        self.category = category
        self.code_input = code_input.strip()
        self.is_source_code = is_source_code  # True: Código fuente, False: TAC
        self.is_valid = is_valid
        self.rule_description = rule_description
        self.expected_behavior = expected_behavior
        self.initial_data = initial_data or {}


# ==============================================================================
# CASOS DE PRUEBA VÁLIDOS (REQUISITO RÚBRICA: 20 PUNTOS)
# ==============================================================================

TEST_VALID_01 = TestCaseCodeGeneration(
    id_num=1,
    title="Mapeo Directo y Asignación de Memoria Aritmética (Ejemplo Rúbrica)",
    category="MAPEO_INSTRUCCIONES",
    code_input="""# Caso oficial de la práctica
t1 = a + b
t2 = t1 * c
result = t2
print result""",
    is_source_code=False,
    is_valid=True,
    rule_description="Traducción de instrucciones TAC (suma y multiplicación) a LOAD, ADD, MUL, STORE con asignación en 0x1000 y 0x2000.",
    expected_behavior="Generación correcta de instrucciones con direcciones 0x1000, 0x1004, 0x1008, 0x100C y ejecución exitosa en la VM con result = (5 + 10) * 2 = 30.",
    initial_data={"a": 5, "b": 10, "c": 2, "result": 0}
)

TEST_VALID_02 = TestCaseCodeGeneration(
    id_num=2,
    title="Optimización de Instrucciones por Encadenamiento de Registros",
    category="OPTIMIZACION",
    code_input="""# Caso de optimización de la rúbrica
t1 = a + b
t2 = t1 + c
result = t2
print result""",
    is_source_code=False,
    is_valid=True,
    rule_description="Optimización de instrucciones: Encadenamiento directo en R1 para evitar almacenamiento y recarga innecesaria de temporales.",
    expected_behavior="Reducción del número de instrucciones generadas mediante encadenamiento en R1 (ADD R1, a; ADD R1, b; ADD R1, c; STORE result, R1) con eficiencia calculada.",
    initial_data={"a": 8, "b": 12, "c": 20, "result": 0}
)

TEST_VALID_03 = TestCaseCodeGeneration(
    id_num=3,
    title="Estructura de Control IF-ELSE con Saltos Condicionales y Etiquetas",
    category="CONTROL_FLUJO",
    code_input="""# Control de flujo con salto condicional
if a > b goto L1
result = 0
goto L2
L1:
result = 1
L2:
print result""",
    is_source_code=False,
    is_valid=True,
    rule_description="Mapeo de saltos condicionales (CMP, JGT, JMP) y resolución de etiquetas L1 y L2 a sus direcciones hexadecimales exactas.",
    expected_behavior="Las etiquetas L1 y L2 son resueltas a direcciones de código válidas (0x10xx) y la VM salta correctamente a L1 dado que a (25) > b (10), asignando result = 1.",
    initial_data={"a": 25, "b": 10, "result": 0}
)

TEST_VALID_04 = TestCaseCodeGeneration(
    id_num=4,
    title="Bucle Iterativo WHILE con Acumulador y Salto Hacia Atrás",
    category="BUCLES",
    code_input="""# Bucle iterativo de conteo y acumulación
L_INICIO:
if contador >= limite goto L_FIN
acum = acum + contador
contador = contador + 1
goto L_INICIO
L_FIN:
result = acum
print result""",
    is_source_code=False,
    is_valid=True,
    rule_description="Generación de ciclos mediante saltos hacia atrás (JMP) y saltos condicionales de salida (JGE) con actualización de memoria.",
    expected_behavior="Ejecución cíclica en la VM sumando 0+1+2+3+4 = 10, con salida final result = 10 y detención en HALT.",
    initial_data={"contador": 0, "limite": 5, "acum": 0, "result": 0}
)

TEST_VALID_05 = TestCaseCodeGeneration(
    id_num=5,
    title="Pipeline Completo de Extremo a Extremo desde Código Fuente",
    category="PIPELINE_COMPLETO",
    code_input="""int a = 14;
int b = 6;
int result = 0;
if (a > b) {
    result = (a + b) * 2;
} else {
    result = a - b;
}
console.log(result);""",
    is_source_code=True,
    is_valid=True,
    rule_description="Compilación completa desde código fuente: Léxico -> Sintáctico AST -> Semántico -> TAC -> Código Máquina -> Binario -> VM.",
    expected_behavior="El compilador procesa el código fuente, genera el TAC, lo traduce a código máquina optimizado, crea el binario y la VM calcula result = (14 + 6) * 2 = 40.",
    initial_data={"a": 14, "b": 6, "result": 0}
)


# ==============================================================================
# CASOS DE PRUEBA INVÁLIDOS (REQUISITO RÚBRICA: 20 PUNTOS)
# ==============================================================================

TEST_INVALID_01 = TestCaseCodeGeneration(
    id_num=6,
    title="Error de Resolución: Salto a Etiqueta No Definida",
    category="ERROR_ETIQUETA",
    code_input="""t1 = a + b
goto L_NO_EXISTE
result = t1""",
    is_source_code=False,
    is_valid=False,
    rule_description="Detección y rechazo de saltos incondicionales o condicionales hacia etiquetas inexistentes en el código.",
    expected_behavior="El asignador de direcciones y la VM interceptan el salto a dirección desconocida 'L_NO_EXISTE' impidiendo una ejecución corrupta.",
    initial_data={"a": 10, "b": 20, "result": 0}
)

TEST_INVALID_02 = TestCaseCodeGeneration(
    id_num=7,
    title="Error de Memoria: Acceso a Variable Desconocida o No Declarada",
    category="ERROR_SIMBOLO",
    code_input="""t1 = a + variable_fantasma_no_declarada
result = t1""",
    is_source_code=False,
    is_valid=False,
    rule_description="Acceso a identificador no asignado en la tabla de símbolos ni en el segmento de datos.",
    expected_behavior="La tabla de símbolos y el evaluador de operandos de la VM detectan la variable sin inicializar y notifican error de operando no reconocido.",
    initial_data={"a": 10, "result": 0}
)

TEST_INVALID_03 = TestCaseCodeGeneration(
    id_num=8,
    title="Error en ALU: División Entre Cero en Instrucción de Máquina",
    category="ERROR_DIVISION_CERO",
    code_input="""t1 = a / 0
result = t1""",
    is_source_code=False,
    is_valid=False,
    rule_description="Detección de división por cero directa en la instrucción de máquina 'DIV Rd, #0'.",
    expected_behavior="La ALU de la Máquina Virtual intercepta la operación ilegal e interrumpe el procesador reportando ZeroDivisionError.",
    initial_data={"a": 50, "result": 0}
)

TEST_INVALID_04 = TestCaseCodeGeneration(
    id_num=9,
    title="Violación de Segmento: Salto a Dirección Fuera de Memoria",
    category="ERROR_SEGMENTACION",
    code_input="""t1 = a + b
goto 0x9999
result = t1""",
    is_source_code=False,
    is_valid=False,
    rule_description="Violación de seguridad de memoria al intentar saltar a una dirección no asignada fuera del segmento 0x1000..0x1FFF.",
    expected_behavior="El cargador o procesador virtual captura la violación de segmento impidiendo la ejecución en direcciones de memoria prohibidas.",
    initial_data={"a": 10, "b": 10, "result": 0}
)

TEST_INVALID_05 = TestCaseCodeGeneration(
    id_num=10,
    title="Fallo de Integridad: Archivo Binario Ejecutable con Firma Corrupta",
    category="ERROR_CABECERA_BINARIA",
    code_input="""# Prueba de rechazo de cabecera binaria inválida
t1 = a + b
result = t1""",
    is_source_code=False,
    is_valid=False,
    rule_description="Verificación de la firma mágica ('MVCO') y checksum en el cargador del sistema operativo.",
    expected_behavior="El cargador del sistema operativo detecta la alteración de la cabecera o checksum y se rehúsa a ejecutar el binario corrupto.",
    initial_data={"a": 10, "b": 10, "result": 0}
)


ALL_TEST_CASES = [
    TEST_VALID_01,
    TEST_VALID_02,
    TEST_VALID_03,
    TEST_VALID_04,
    TEST_VALID_05,
    TEST_INVALID_01,
    TEST_INVALID_02,
    TEST_INVALID_03,
    TEST_INVALID_04,
    TEST_INVALID_05
]

VALID_TEST_CASES = [t for t in ALL_TEST_CASES if t.is_valid]
INVALID_TEST_CASES = [t for t in ALL_TEST_CASES if not t.is_valid]

