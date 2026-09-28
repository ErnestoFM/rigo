"""
================================================================================
ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import List, Dict, Any


class TestCaseItem:
    """
    Representa un caso de prueba individual con metadatos descriptivos y regla evaluada.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, id_num: int, title: str, code: str, is_valid: bool, rule_description: str, expected_behavior: str):
        self.id_num = id_num
        self.title = title
        self.code = code.strip()
        self.is_valid = is_valid
        self.rule_description = rule_description
        self.expected_behavior = expected_behavior


# ==============================================================================
# CASOS DE PRUEBA VÁLIDOS (SINTAXIS CORRECTA CONFORME A LA GRAMÁTICA)
# ==============================================================================

TEST_VALID_CLASS_OFFICIAL = """class MiClase {
    int miMetodo(int a, float b) {
        // cuerpo del método
    }
    void otroMetodo() {
        // cuerpo del método
    }
}"""

TEST_VALID_CLASS_WITH_VARIABLES = """class Rectangulo {
    float base;
    float altura;

    float calcularArea() {
        return base * altura;
    }

    void setDimensiones(float b, float h) {
        base = b;
        altura = h;
    }
}"""

TEST_VALID_MULTIPLE_CLASSES = """class Punto {
    int x;
    int y;

    void mover(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }
}

class Circulo {
    float radio;

    float calcularArea() {
        return 3.1416 * radio * radio;
    }
}"""

TEST_VALID_COMPLEX_BODY = """class Validador {
    boolean esMayor(int edad, int limite) {
        if (edad >= limite) {
            return true;
        } else {
            return false;
        }
    }

    int sumarSecuencia(int n) {
        int total = 0;
        int i = 1;
        while (i <= n) {
            total = total + i;
            i = i + 1;
        }
        return total;
    }
}"""

TEST_VALID_CUSTOM_TYPES = """class GestorEstudiante {
    Persona estudiante;

    Persona obtenerEstudiante() {
        return estudiante;
    }

    void asignarEstudiante(Persona p) {
        estudiante = p;
    }
}"""

TEST_VALID_EMPTY_MEMBERS = """class ContenedorVacio {
    void accionInerte() {
    }
}"""


# ==============================================================================
# CASOS DE PRUEBA INVÁLIDOS (DETECCIÓN Y GESTIÓN DE ERRORES SINTÁCTICOS)
# ==============================================================================

# 1. Caso Oficial del Profesor: Falta coma entre parámetros
TEST_INVALID_MISSING_COMMA_PARAMS = """class MiClase {
    int miMetodo(int a float b) {
        // Falta coma entre parámetros
    }
    void otroMetodo() {
    }
}"""

# 2. Caso Oficial del Profesor: Faltan paréntesis en declaración de método
TEST_INVALID_MISSING_PARENTHESES = """class MiClase {
    void otroMetodo {
        // Faltan paréntesis
    }
}"""

# 3. Caso Oficial de la Rúbrica: Cuerpo de clase inválido
TEST_INVALID_CLASS_BODY = """class MiClase int x; float y;"""

# 4. Caso Oficial de la Rúbrica: Tipo de retorno inválido
TEST_INVALID_RETURN_TYPE = """class MiClase {
    123 miMetodo(int a, float b) {
        return a;
    }
}"""

# 5. Caso Oficial de la Rúbrica: Parámetro inválido (falta identificador)
TEST_INVALID_PARAMETER_NO_NAME = """class MiClase {
    void procesar(int) {
        // Falta el nombre del parámetro
    }
}"""

# 6. Llaves desbalanceadas: falta '}' de cierre de clase
TEST_INVALID_UNBALANCED_CLASS_BRACE = """class MiClase {
    void miMetodo() {
        return;
    }
"""

# 7. Llaves desbalanceadas: falta '}' de cierre del método
TEST_INVALID_UNBALANCED_METHOD_BRACE = """class MiClase {
    int calcularTotal(int a, int b) {
        return a + b;
}"""

# 8. Nombre de clase inválido (falta identificador después de 'class')
TEST_INVALID_MISSING_CLASS_NAME = """class {
    int variable;
}"""

# 9. Declaración de variable inválida en la clase (falta identificador)
TEST_INVALID_VAR_DECLARATION = """class MiClase {
    int ;
}"""

# 10. Sentencia inválida dentro del cuerpo del método
TEST_INVALID_METHOD_STATEMENT = """class MiClase {
    void ejecutar() {
        int = 50;
    }
}"""


# ==============================================================================
# BATERÍA CONSOLIDADA DE CASOS DE PRUEBA
# ==============================================================================

VALID_TEST_CASES: List[TestCaseItem] = [
    TestCaseItem(
        id_num=1,
        title="Caso Válido Oficial: Definición de Clases y Métodos Estándar",
        code=TEST_VALID_CLASS_OFFICIAL,
        is_valid=True,
        rule_description="clase -> 'class' identificador '{' cuerpo_clase '}'",
        expected_behavior="Generación de AST con clase 'MiClase', método 'miMetodo' (2 params) y método 'otroMetodo' (0 params) sin errores."
    ),
    TestCaseItem(
        id_num=2,
        title="Caso Válido: Clase con Atributos de Instancia y Métodos de Cálculo",
        code=TEST_VALID_CLASS_WITH_VARIABLES,
        is_valid=True,
        rule_description="cuerpo_clase -> ( declaracion_metodo | declaracion_variable )*",
        expected_behavior="Identificación de atributos 'base' y 'altura' junto con métodos 'calcularArea' y 'setDimensiones'."
    ),
    TestCaseItem(
        id_num=3,
        title="Caso Válido: Múltiples Clases en un Mismo Archivo Fuente",
        code=TEST_VALID_MULTIPLE_CLASSES,
        is_valid=True,
        rule_description="programa -> ( clase )*",
        expected_behavior="Análisis sintáctico exitoso de clases consecutivas 'Punto' y 'Circulo' con sus miembros."
    ),
    TestCaseItem(
        id_num=4,
        title="Caso Válido: Métodos con Sentencias de Control (if, while) y Expresiones",
        code=TEST_VALID_COMPLEX_BODY,
        is_valid=True,
        rule_description="cuerpo_metodo -> ( sentencia )*",
        expected_behavior="Construcción completa de nodos IfNode, WhileNode, ReturnNode y asignaciones dentro de métodos."
    ),
    TestCaseItem(
        id_num=5,
        title="Caso Válido: Tipos Definidos por el Usuario (Objetos como Tipo)",
        code=TEST_VALID_CUSTOM_TYPES,
        is_valid=True,
        rule_description="tipo -> 'int' | 'float' | 'void' | 'char' | 'boolean' | identificador",
        expected_behavior="Reconocimiento del identificador 'Persona' como tipo de retorno y tipo de parámetro válido."
    ),
    TestCaseItem(
        id_num=6,
        title="Caso Válido: Clase y Método con Cuerpo Vacío",
        code=TEST_VALID_EMPTY_MEMBERS,
        is_valid=True,
        rule_description="cuerpo_metodo -> ( sentencia )* (donde secuencia puede ser vacía)",
        expected_behavior="Aceptación sintáctica de bloques de código vacíos sin fallos."
    )
]

INVALID_TEST_CASES: List[TestCaseItem] = [
    TestCaseItem(
        id_num=7,
        title="Caso Inválido Oficial 1: Falta de Coma entre Parámetros",
        code=TEST_INVALID_MISSING_COMMA_PARAMS,
        is_valid=False,
        rule_description="parametros -> ( parametro ( ',' parametro )* )?",
        expected_behavior="Reporte: 'Error: Parámetro inválido en la declaración de método en la línea 2, columna 18. Falta coma entre parámetros.'"
    ),
    TestCaseItem(
        id_num=8,
        title="Caso Inválido Oficial 2: Faltan Paréntesis en Declaración de Método",
        code=TEST_INVALID_MISSING_PARENTHESES,
        is_valid=False,
        rule_description="declaracion_metodo -> tipo identificador '(' parametros ')' '{' cuerpo_metodo '}'",
        expected_behavior="Reporte: 'Error: Falta paréntesis en la declaración de método en la línea 2, columna 21.'"
    ),
    TestCaseItem(
        id_num=9,
        title="Caso Inválido Oficial Rúbrica: Cuerpo de Clase Inválido",
        code=TEST_INVALID_CLASS_BODY,
        is_valid=False,
        rule_description="clase -> 'class' identificador '{' cuerpo_clase '}'",
        expected_behavior="Reporte: 'Error: Cuerpo de clase inválido en la declaración de 'class' en la línea 1, columna 15.'"
    ),
    TestCaseItem(
        id_num=10,
        title="Caso Inválido Oficial Rúbrica: Tipo de Retorno Inválido",
        code=TEST_INVALID_RETURN_TYPE,
        is_valid=False,
        rule_description="tipo -> 'int' | 'float' | 'void' | 'char' | 'boolean' | identificador",
        expected_behavior="Reporte: 'Error: Tipo de retorno inválido en la declaración de método en la línea 2, columna 5.'"
    ),
    TestCaseItem(
        id_num=11,
        title="Caso Inválido Oficial Rúbrica: Parámetro Inválido (Sin Nombre)",
        code=TEST_INVALID_PARAMETER_NO_NAME,
        is_valid=False,
        rule_description="parametro -> tipo identificador",
        expected_behavior="Reporte: 'Error: Parámetro inválido en la declaración de método en la línea 2, columna 23.'"
    ),
    TestCaseItem(
        id_num=12,
        title="Caso Inválido: Llaves Desbalanceadas en Clase (Falta '}')",
        code=TEST_INVALID_UNBALANCED_CLASS_BRACE,
        is_valid=False,
        rule_description="Delimitación de bloque de clase con llave de cierre obligatoria",
        expected_behavior="Reporte: 'Error: Llaves desbalanceadas o falta '}' de cierre en la línea 6, columna 1.'"
    ),
    TestCaseItem(
        id_num=13,
        title="Caso Inválido: Llaves Desbalanceadas en Método (Falta '}')",
        code=TEST_INVALID_UNBALANCED_METHOD_BRACE,
        is_valid=False,
        rule_description="Delimitación de cuerpo de método con llave de cierre obligatoria",
        expected_behavior="Reporte: 'Error: Llaves desbalanceadas o falta '}' de cierre en la línea 4, columna 1.'"
    ),
    TestCaseItem(
        id_num=14,
        title="Caso Inválido: Nombre de Clase Omitido o Inválido",
        code=TEST_INVALID_MISSING_CLASS_NAME,
        is_valid=False,
        rule_description="clase -> 'class' identificador '{' cuerpo_clase '}'",
        expected_behavior="Reporte: 'Error: Falta identificador (nombre) en la declaración de clase en la línea 1, columna 7.'"
    ),
    TestCaseItem(
        id_num=15,
        title="Caso Inválido: Declaración de Variable Inválida en Clase",
        code=TEST_INVALID_VAR_DECLARATION,
        is_valid=False,
        rule_description="declaracion_variable -> tipo identificador ';'",
        expected_behavior="Reporte: 'Error: Parámetro inválido o falta identificador en la línea 2, columna 9.'"
    ),
    TestCaseItem(
        id_num=16,
        title="Caso Inválido: Sentencia Inválida en Cuerpo de Método",
        code=TEST_INVALID_METHOD_STATEMENT,
        is_valid=False,
        rule_description="sentencia -> declaracion_variable | sentencia_asignacion | ...",
        expected_behavior="Reporte: 'Error: Sentencia inválida en el cuerpo del método en la línea 3, columna 9.'"
    )
]

ALL_TEST_CASES = VALID_TEST_CASES + INVALID_TEST_CASES
