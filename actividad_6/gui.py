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

import tkinter as tk
from tkinter import ttk, scrolledtext
from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import ALL_TEST_CASES, TestCaseItem


class SyntaxAnalyzerClassesAndMethodsGUI:
    """
    Interfaz Gráfica de Usuario (GUI) interactiva para el Analizador Sintáctico
    de Métodos y Clases con visualización de AST y diagnóstico de errores sintácticos.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Compilador - Actividad 6: Análisis Sintáctico de Métodos y Clases")
        self.root.geometry("1220x860")
        self.root.minsize(1050, 720)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.root.configure(bg="#181825")

        self._prepare_cases_map()
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Cargar caso oficial 1 por defecto
        first_case_key = list(self.cases_map.keys())[0]
        self._load_selected_case(first_case_key)

    def _prepare_cases_map(self):
        self.cases_map = {}
        for test in ALL_TEST_CASES:
            tipo = "VÁLIDO" if test.is_valid else "INVÁLIDO"
            key = f"[{tipo}] Caso {test.id_num:02d}: {test.title}"
            self.cases_map[key] = test

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e1e2e", padx=18, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="ACTIVIDAD 6: ANÁLISIS SINTÁCTICO DE MÉTODOS Y CLASES",
            font=("Segoe UI", 13, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa"
        )
        title_label.pack(anchor="w")

        subtitle = "Profesor: Rigoberto Cárdenas Larios  |  Traductores de Lenguaje / Compiladores\n" \
                   "Integrantes del Equipo (Orden Alfabético por Primer Apellido):\n" \
                   "1. DIAZ TORRES JAZMIN MONTSERRAT  |  2. FIERRO MELÉNDEZ ERNESTO HATUEY\n" \
                   "3. HERNANDEZ GARCIA HECTOR GABRIEL  |  4. MILLAN GUERRERO OSWALDO JOSUE"

        members_label = tk.Label(
            header_frame,
            text=subtitle,
            font=("Segoe UI", 9),
            bg="#1e1e2e",
            fg="#cdd6f4",
            justify="left"
        )
        members_label.pack(anchor="w", pady=(4, 0))

    def _create_main_content(self):
        main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL, bg="#181825", sashwidth=6, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # ---------------- Panel Superior: Editor y Controles ----------------
        top_frame = tk.Frame(main_pane, bg="#181825")
        main_pane.add(top_frame, minsize=260)

        control_frame = tk.Frame(top_frame, bg="#181825")
        control_frame.pack(fill=tk.X, pady=(0, 6))

        lbl_select = tk.Label(control_frame, text="Cargar Caso de Prueba:", font=("Segoe UI", 10, "bold"), bg="#181825", fg="#a6adc8")
        lbl_select.pack(side=tk.LEFT, padx=(0, 8))

        self.case_combobox = ttk.Combobox(
            control_frame,
            values=list(self.cases_map.keys()),
            state="readonly",
            width=65,
            font=("Segoe UI", 9)
        )
        self.case_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.case_combobox.bind("<<ComboboxSelected>>", lambda e: self._load_selected_case(self.case_combobox.get()))

        btn_analyze = tk.Button(
            control_frame,
            text="▶ ANALIZAR SINTAXIS",
            command=self.analyze_code,
            font=("Segoe UI", 10, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            padx=14,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_analyze.pack(side=tk.LEFT, padx=4)

        btn_clear = tk.Button(
            control_frame,
            text="Limpiar",
            command=self._clear_editor,
            font=("Segoe UI", 9),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            padx=10,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_clear.pack(side=tk.LEFT, padx=4)

        # Editor de Código Fuente
        lbl_code = tk.Label(top_frame, text="Código Fuente del Lenguaje (Clases y Métodos):", font=("Segoe UI", 9, "bold"), bg="#181825", fg="#89b4fa")
        lbl_code.pack(anchor="w", pady=(2, 2))

        self.txt_source = scrolledtext.ScrolledText(
            top_frame,
            height=10,
            font=("Consolas", 11),
            bg="#11111b",
            fg="#cdd6f4",
            insertbackground="#f5e0dc",
            selectbackground="#45475a",
            padx=8,
            pady=8
        )
        self.txt_source.pack(fill=tk.BOTH, expand=True)

        # ---------------- Panel Inferior: Pestañas de Resultados ----------------
        bottom_frame = tk.Frame(main_pane, bg="#181825")
        main_pane.add(bottom_frame, minsize=320)

        self.notebook = ttk.Notebook(bottom_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Árbol AST
        tab_ast = tk.Frame(self.notebook, bg="#11111b")
        self.notebook.add(tab_ast, text=" 🌳 Árbol Sintáctico (AST) ")
        self.txt_ast = scrolledtext.ScrolledText(
            tab_ast,
            font=("Consolas", 10),
            bg="#11111b",
            fg="#a6e3a1",
            padx=10,
            pady=10
        )
        self.txt_ast.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Errores Sintácticos
        tab_errors = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(tab_errors, text=" ❌ Errores Sintácticos ")

        cols_err = ("num", "linea", "col", "cat", "msg", "sugg")
        self.tree_errors = ttk.Treeview(tab_errors, columns=cols_err, show="headings", height=8)
        self.tree_errors.heading("num", text="#")
        self.tree_errors.heading("linea", text="Línea")
        self.tree_errors.heading("col", text="Columna")
        self.tree_errors.heading("cat", text="Categoría")
        self.tree_errors.heading("msg", text="Mensaje de Error")
        self.tree_errors.heading("sugg", text="Sugerencia Pedagógica")

        self.tree_errors.column("num", width=40, anchor="center")
        self.tree_errors.column("linea", width=60, anchor="center")
        self.tree_errors.column("col", width=65, anchor="center")
        self.tree_errors.column("cat", width=220, anchor="w")
        self.tree_errors.column("msg", width=360, anchor="w")
        self.tree_errors.column("sugg", width=420, anchor="w")

        scroll_err = ttk.Scrollbar(tab_errors, orient=tk.VERTICAL, command=self.tree_errors.yview)
        self.tree_errors.configure(yscrollcommand=scroll_err.set)
        self.tree_errors.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_err.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña 3: Tokens Léxicos
        tab_tokens = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(tab_tokens, text=" 🔍 Tokens Léxicos ")

        cols_tok = ("num", "val", "tipo", "linea", "col")
        self.tree_tokens = ttk.Treeview(tab_tokens, columns=cols_tok, show="headings", height=8)
        self.tree_tokens.heading("num", text="#")
        self.tree_tokens.heading("val", text="Lexema / Valor")
        self.tree_tokens.heading("tipo", text="Tipo de Token")
        self.tree_tokens.heading("linea", text="Línea")
        self.tree_tokens.heading("col", text="Columna")

        self.tree_tokens.column("num", width=50, anchor="center")
        self.tree_tokens.column("val", width=260, anchor="w")
        self.tree_tokens.column("tipo", width=240, anchor="w")
        self.tree_tokens.column("linea", width=80, anchor="center")
        self.tree_tokens.column("col", width=80, anchor="center")

        scroll_tok = ttk.Scrollbar(tab_tokens, orient=tk.VERTICAL, command=self.tree_tokens.yview)
        self.tree_tokens.configure(yscrollcommand=scroll_tok.set)
        self.tree_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tok.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña 4: Gramática Oficial EBNF
        tab_grammar = tk.Frame(self.notebook, bg="#11111b")
        self.notebook.add(tab_grammar, text=" 📜 Reglas de la Gramática (EBNF) ")
        self.txt_grammar = scrolledtext.ScrolledText(
            tab_grammar,
            font=("Consolas", 10),
            bg="#11111b",
            fg="#89b4fa",
            padx=12,
            pady=12
        )
        self.txt_grammar.pack(fill=tk.BOTH, expand=True)
        self._load_grammar_help()

    def _create_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg="#1e1e2e", padx=12, pady=6)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_status = tk.Label(
            self.status_bar,
            text="Listo para analizar.",
            font=("Segoe UI", 9, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        self.lbl_status.pack(side=tk.LEFT)

        self.lbl_rule_info = tk.Label(
            self.status_bar,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg="#1e1e2e",
            fg="#9399b2"
        )
        self.lbl_rule_info.pack(side=tk.RIGHT)

    def _load_grammar_help(self):
        grammar_doc = """================================================================================
GRAMÁTICA FORMAL PARA MÉTODOS Y CLASES (EBNF)
MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS
================================================================================

1. Regla Principal de Programa:
   programa            -> ( clase | declaracion_metodo | declaracion_variable )*

2. Definición de Clase:
   clase               -> 'class' identificador '{' cuerpo_clase '}'
   cuerpo_clase        -> ( declaracion_metodo | declaracion_variable )*

3. Definición de Métodos:
   declaracion_metodo  -> tipo identificador '(' parametros ')' '{' cuerpo_metodo '}'
   parametros          -> ( parametro ( ',' parametro )* )?
   parametro           -> tipo identificador

4. Definición de Variables y Miembros:
   declaracion_variable-> tipo identificador ( '=' expresion )? ';'

5. Tipos de Datos:
   tipo                -> 'int' | 'float' | 'void' | 'char' | 'boolean' | identificador

6. Cuerpo de Método y Sentencias:
   cuerpo_metodo       -> ( sentencia )*
   sentencia           -> declaracion_variable
                        | sentencia_asignacion
                        | sentencia_retorno
                        | sentencia_if
                        | sentencia_while
                        | llamada_metodo ';'
                        | bloque_sentencias
                        | ';'

   sentencia_asignacion-> identificador '=' expresion ';'
   sentencia_retorno   -> 'return' ( expresion )? ';'
   sentencia_if        -> 'if' '(' expresion ')' sentencia ( 'else' sentencia )?
   sentencia_while     -> 'while' '(' expresion ')' sentencia
   bloque_sentencias   -> '{' ( sentencia )* '}'
   llamada_metodo      -> identificador '(' argumentos ')'
   argumentos          -> ( expresion ( ',' expresion )* )?

7. Nombres y Literales:
   identificador       -> [a-zA-Z_][a-zA-Z0-9_]*
"""
        self.txt_grammar.insert(tk.END, grammar_doc)
        self.txt_grammar.config(state=tk.DISABLED)

    def _load_selected_case(self, key: str):
        test = self.cases_map.get(key)
        if not test:
            return
        self.case_combobox.set(key)
        self.txt_source.delete("1.0", tk.END)
        self.txt_source.insert(tk.END, test.code)
        self.lbl_rule_info.config(text=f"Regla: {test.rule_description}")
        self.analyze_code()

    def _clear_editor(self):
        self.txt_source.delete("1.0", tk.END)
        self.txt_ast.delete("1.0", tk.END)
        for row in self.tree_errors.get_children():
            self.tree_errors.delete(row)
        for row in self.tree_tokens.get_children():
            self.tree_tokens.delete(row)
        self.lbl_status.config(text="Editor limpio.", fg="#cdd6f4")
        self.lbl_rule_info.config(text="")

    def analyze_code(self):
        code = self.txt_source.get("1.0", tk.END).strip()
        if not code:
            self.lbl_status.config(text="Advertencia: El editor está vacío.", fg="#f9e2af")
            return

        # 1. Análisis Léxico
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Limpiar tabla de tokens
        for row in self.tree_tokens.get_children():
            self.tree_tokens.delete(row)

        for i, tok in enumerate(tokens, 1):
            if tok.type.name != "EOF":
                self.tree_tokens.insert("", tk.END, values=(i, tok.value, tok.type.name, tok.line, tok.column))

        # 2. Análisis Sintáctico
        error_handler = SyntaxErrorHandler()
        parser = Parser(tokens, error_handler)
        ast = parser.parse()

        # Limpiar tabla de errores y texto de AST
        for row in self.tree_errors.get_children():
            self.tree_errors.delete(row)
        self.txt_ast.delete("1.0", tk.END)

        if not error_handler.has_errors():
            self.txt_ast.insert(tk.END, ast.to_tree_str())
            self.lbl_status.config(
                text="✔ ESTADO SINTÁCTICO: [CORRECTO] (0 Errores detectados)",
                fg="#a6e3a1"
            )
            self.notebook.select(0) # Pestaña de AST
        else:
            self.lbl_status.config(
                text=f"❌ ESTADO SINTÁCTICO: [ERROR SINTÁCTICO] ({len(error_handler.errors)} Error(es) detectado(s))",
                fg="#f38ba8"
            )
            for i, err in enumerate(error_handler.errors, 1):
                self.tree_errors.insert(
                    "",
                    tk.END,
                    values=(i, err.line, err.column, err.category, err.message, err.suggestion)
                )

            # Mostrar AST parcial si existe
            if ast:
                self.txt_ast.insert(tk.END, "--- ÁRBOL PARCIAL O CON ERRORES ---\n\n")
                self.txt_ast.insert(tk.END, ast.to_tree_str())

            self.notebook.select(1) # Pestaña de Errores


def main():
    root = tk.Tk()
    app = SyntaxAnalyzerClassesAndMethodsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
