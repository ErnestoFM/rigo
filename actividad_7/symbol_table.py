"""
================================================================================
ACTIVIDAD 7: ANÁLISIS SEMÁNTICO - TABLA DE SÍMBOLOS Y TIPOS DE DATOS
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

from typing import Dict, Any, Optional, List, Tuple


class Symbol:
    """
    Representa una entrada individual en la tabla de símbolos conforme a la rúbrica:
    identificador -> { tipo: tipo_de_dato, alcance: global | local, valor: valor_asignado, ... }

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(
        self,
        name: str,
        data_type: str,
        scope_type: str = "global",
        scope_name: str = "global",
        scope_level: int = 0,
        value: Any = None,
        line: int = 1,
        column: int = 1,
        is_function: bool = False,
        params: Optional[List[Tuple[str, str]]] = None
    ):
        self.name = name
        self.data_type = data_type
        self.scope_type = scope_type  # 'global' o 'local'
        self.scope_name = scope_name  # e.g., 'global', 'miFuncion', 'bloque_L12'
        self.scope_level = scope_level  # 0: global, 1: función, 2+: bloques anidados
        self.value = value
        self.line = line
        self.column = column
        self.is_function = is_function
        self.params = params or []

    def to_dict(self) -> Dict[str, Any]:
        """Estructura de diccionario requerida explícitamente en el ejemplo de la rúbrica."""
        return {
            "identificador": self.name,
            "tipo": self.data_type,
            "alcance": self.scope_type,
            "ambito_nombre": self.scope_name,
            "nivel": self.scope_level,
            "valor": self.value if self.value is not None else "(no asignado)",
            "linea": self.line,
            "columna": self.column
        }

    def __repr__(self) -> str:
        val_str = f" = {self.value}" if self.value is not None else ""
        return f"<Symbol {self.name}: {self.data_type} [{self.scope_type}:{self.scope_name}]{val_str} (L:{self.line}, C:{self.column})>"


class Scope:
    """
    Representa un entorno o ámbito léxico (global o local), organizado
    jerárquicamente para permitir anidamiento, herencia y enmascaramiento.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, name: str, scope_type: str = "local", level: int = 1, parent: Optional['Scope'] = None):
        self.name = name
        self.scope_type = scope_type  # 'global' o 'local'
        self.level = level
        self.parent = parent
        self.children: List['Scope'] = []
        self.symbols: Dict[str, Symbol] = {}

        if parent:
            parent.children.append(self)

    def define(self, symbol: Symbol) -> bool:
        """Inserta un símbolo en el ámbito actual si no existe colisión previa."""
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup_current(self, name: str) -> Optional[Symbol]:
        """Busca el símbolo exclusivamente en el ámbito actual."""
        return self.symbols.get(name)

    def lookup(self, name: str) -> Optional[Symbol]:
        """Busca el símbolo en el ámbito actual y, recursivamente, en los ámbitos padres."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class SymbolTable:
    """
    Gestor Central de la Tabla de Símbolos y Entornos de Ámbito.
    Implementa las funciones especificadas en la rúbrica oficial:
    - inserten_simbolo(identificador, tipo_de_dato, alcance)
    - busquen_simbolo(identificador)
    - Gestión jerárquica de ámbitos globales y locales.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self):
        self.global_scope = Scope(name="global", scope_type="global", level=0, parent=None)
        self.current_scope: Scope = self.global_scope
        self.all_scopes: List[Scope] = [self.global_scope]
        self.all_symbols_history: List[Symbol] = []

    def reset(self):
        """Reinicia la tabla de símbolos para una nueva corrida."""
        self.global_scope = Scope(name="global", scope_type="global", level=0, parent=None)
        self.current_scope = self.global_scope
        self.all_scopes = [self.global_scope]
        self.all_symbols_history.clear()

    def enter_scope(self, name: str, scope_type: str = "local") -> Scope:
        """Crea y entra a un nuevo ámbito hijo (función o bloque de sentencias)."""
        new_scope = Scope(
            name=name,
            scope_type=scope_type,
            level=self.current_scope.level + 1,
            parent=self.current_scope
        )
        self.all_scopes.append(new_scope)
        self.current_scope = new_scope
        return new_scope

    def exit_scope(self) -> Scope:
        """Sale del ámbito actual retornando al ámbito padre."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        return self.current_scope

    def inserten_simbolo(
        self,
        identificador: str,
        tipo_de_dato: str,
        alcance: Optional[str] = None,
        valor: Any = None,
        linea: int = 1,
        columna: int = 1,
        is_function: bool = False,
        params: Optional[List[Tuple[str, str]]] = None
    ) -> Tuple[bool, Optional[Symbol]]:
        """
        Función oficial de inserción de símbolos en la tabla.
        Retorna (True, symbol) si se insertó con éxito, o (False, existing_symbol) si ya existía en este ámbito.
        """
        scope_t = alcance or self.current_scope.scope_type
        sym = Symbol(
            name=identificador,
            data_type=tipo_de_dato,
            scope_type=scope_t,
            scope_name=self.current_scope.name,
            scope_level=self.current_scope.level,
            value=valor,
            line=linea,
            column=columna,
            is_function=is_function,
            params=params
        )

        success = self.current_scope.define(sym)
        if success:
            self.all_symbols_history.append(sym)
            return True, sym
        return False, self.current_scope.lookup_current(identificador)

    # Alias en español conforme a la rúbrica
    def insertar_simbolo(self, *args, **kwargs):
        return self.inserten_simbolo(*args, **kwargs)

    def busquen_simbolo(self, identificador: str) -> Optional[Symbol]:
        """
        Función oficial de búsqueda de símbolos en la tabla.
        Busca desde el ámbito actual hacia arriba (global).
        """
        return self.current_scope.lookup(identificador)

    # Alias en español conforme a la rúbrica
    def buscar_simbolo(self, identificador: str) -> Optional[Symbol]:
        return self.busquen_simbolo(identificador)

    def update_symbol_value(self, name: str, value: Any) -> bool:
        """Actualiza el valor asignado a un identificador en el ámbito correspondiente."""
        sym = self.busquen_simbolo(name)
        if sym:
            sym.value = value
            return True
        return False

    def get_all_registered_symbols(self) -> List[Symbol]:
        """Devuelve todos los símbolos únicos registrados en orden de declaración."""
        return self.all_symbols_history

    def to_formatted_table(self) -> str:
        """Genera una representación tabular ASCII comprensible a simple vista."""
        symbols = self.get_all_registered_symbols()
        if not symbols:
            return "Tabla de símbolos vacía (no se registraron identificadores)."

        sep = "+" + "-" * 5 + "+" + "-" * 18 + "+" + "-" * 10 + "+" + "-" * 10 + "+" + "-" * 16 + "+" + "-" * 7 + "+" + "-" * 16 + "+" + "-" * 11 + "+"
        header = f"| {'#':<3} | {'IDENTIFICADOR':<16} | {'TIPO':<8} | {'ALCANCE':<8} | {'ÁMBITO':<14} | {'NIVEL':<5} | {'VALOR ASIGNADO':<14} | {'LÍNEA:COL':<9} |"
        rows = [sep, header, sep]

        for idx, sym in enumerate(symbols, 1):
            val_display = str(sym.value) if sym.value is not None else "(indefinido)"
            if len(val_display) > 14:
                val_display = val_display[:11] + "..."
            loc_str = f"L:{sym.line}, C:{sym.column}"
            rows.append(
                f"| {idx:<3} | {sym.name:<16} | {sym.data_type:<8} | {sym.scope_type:<8} | {sym.scope_name:<14} | {sym.scope_level:<5} | {val_display:<14} | {loc_str:<9} |"
            )
        rows.append(sep)

        # Resumen de ámbitos y variables
        globals_cnt = sum(1 for s in symbols if s.scope_type == "global")
        locals_cnt = sum(1 for s in symbols if s.scope_type == "local")
        rows.append(f"\n  RESUMEN DE SÍMBOLOS: Total = {len(symbols)} | Variables Globales = {globals_cnt} | Variables Locales = {locals_cnt}")

        return "\n".join(rows)
