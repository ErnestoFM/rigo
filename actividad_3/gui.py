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

import tkinter as tk
from tkinter import ttk, scrolledtext
from lexer import Lexer
from parser import Parser
from error_handler import SyntaxErrorHandler
from test_cases import (
    TEST_VALID_SIMPLE_VARS,
    TEST_VALID_INITIALIZED_VARS,
    TEST_VALID_CONSTANTS,
    TEST_VALID_USAGE_EXPRESSIONS,
    TEST_INVALID_IDENTIFIERS,
    TEST_INVALID_TYPES,
    TEST_MISSING_SEMICOLONS,
    TEST_UNINITIALIZED_CONSTANT,
    TEST_MALFORMED_ASSIGNMENT,
    TEST_COMBINED_ERRORS
)

class SyntaxAnalyzerGUI:
    """
    Interfaz Gráfica de Usuario (GUI) para la demostración interactiva
    del Analizador Sintáctico de Variables y Constantes.
    
    Integrantes:
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """

    TEST_SUITES = {
        "1. Válido: Declaraciones Simples": TEST_VALID_SIMPLE_VARS,
        "2. Válido: Declaraciones con Inicialización": TEST_VALID_INITIALIZED_VARS,
        "3. Válido: Constantes Inicializadas": TEST_VALID_CONSTANTS,
        "4. Válido: Uso de Variables en Expresiones": TEST_VALID_USAGE_EXPRESSIONS,
        "5. Error: Identificadores Inválidos (123x)": TEST_INVALID_IDENTIFIERS,
        "6. Error: Tipos de Datos No Válidos": TEST_INVALID_TYPES,
        "7. Error: Falta de Punto y Coma (;)": TEST_MISSING_SEMICOLONS,
        "8. Error: Constante No Inicializada": TEST_UNINITIALIZED_CONSTANT,
        "9. Error: Expresión Rota / Incompleta": TEST_MALFORMED_ASSIGNMENT,
        "10. Suite Integral: Múltiples Errores Combinados": TEST_COMBINED_ERRORS
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Compilador - Actividad 3: Análisis Sintáctico de Variables y Constantes")
        self.root.geometry("1180x820")
        self.root.minsize(980, 680)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        BG_COLOR = "#181825"
        self.root.configure(bg=BG_COLOR)

        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Cargar caso combinado por defecto y analizar
        self._load_selected_suite("10. Suite Integral: Múltiples Errores Combinados")

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e1e2e", padx=15, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame, 
            text="ACTIVIDAD 3: ANÁLISIS SINTÁCTICO DE VARIABLES Y CONSTANTES", 
            font=("Segoe UI", 14, "bold"), 
            bg="#1e1e2e", 
            fg="#89b4fa"
        )
        title_label.pack(anchor="w")

        subtitle = "Integrantes del Equipo (Orden Alfabético por Primer Apellido):\n" \
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

        lbl_select = tk.Label(control_frame, text="Casos de Prueba:", font=("Segoe UI", 10, "bold"), bg="#181825", fg="#a6adc8")
        lbl_select.pack(side=tk.LEFT, padx=(0, 8))

        self.suite_var = tk.StringVar(value="10. Suite Integral: Múltiples Errores Combinados")
        suite_combo = ttk.Combobox(
            control_frame, 
            textvariable=self.suite_var, 
            values=list(self.TEST_SUITES.keys()), 
            state="readonly", 
            width=48,
            font=("Segoe UI", 9)
        )
        suite_combo.pack(side=tk.LEFT, padx=(0, 10))
        suite_combo.bind("<<ComboboxSelected>>", lambda e: self._load_selected_suite(self.suite_var.get()))

        btn_analyze = tk.Button(
            control_frame, 
            text="▶ ANALIZAR SINTAXIS", 
            command=self.analyze_code, 
            font=("Segoe UI", 9, "bold"), 
            bg="#a6e3a1", 
            fg="#11111b", 
            activebackground="#94e2d5", 
            padx=14, 
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_analyze.pack(side=tk.LEFT, padx=5)

        btn_clear = tk.Button(
            control_frame, 
            text="Limpiar Editor", 
            command=self._clear_editor, 
            font=("Segoe UI", 9), 
            bg="#45475a", 
            fg="#cdd6f4", 
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_clear.pack(side=tk.LEFT, padx=5)

        # Editor de Código
        editor_label = tk.Label(top_frame, text="Código Fuente de Entrada:", font=("Segoe UI", 9, "bold"), bg="#181825", fg="#cdd6f4")
        editor_label.pack(anchor="w")

        self.code_editor = scrolledtext.ScrolledText(
            top_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 11), 
            bg="#11111b", 
            fg="#cdd6f4", 
            insertbackground="#f5e0dc", 
            height=9,
            relief=tk.FLAT,
            padx=8,
            pady=8
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # ---------------- Panel Inferior: Pestañas de Resultados ----------------
        bottom_frame = tk.Frame(main_pane, bg="#181825")
        main_pane.add(bottom_frame, minsize=320)

        notebook = ttk.Notebook(bottom_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Árbol de Sintaxis Abstracta (AST)
        tab_ast = tk.Frame(notebook, bg="#11111b")
        notebook.add(tab_ast, text="  🌳 Árbol Sintáctico (AST)  ")

        self.ast_text = scrolledtext.ScrolledText(
            tab_ast, 
            font=("Consolas", 10), 
            bg="#11111b", 
            fg="#89b4fa", 
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.ast_text.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Errores Sintácticos
        tab_errors = tk.Frame(notebook, bg="#181825")
        notebook.add(tab_errors, text="  ❌ Errores Sintácticos  ")

        error_cols = ("#", "Línea", "Columna", "Token", "Descripción del Error", "Sugerencia de Corrección")
        self.error_tree = ttk.Treeview(tab_errors, columns=error_cols, show="headings", selectmode="browse")
        
        col_widths = {"#": 45, "Línea": 65, "Columna": 65, "Token": 110, "Descripción del Error": 360, "Sugerencia de Corrección": 400}
        for col in error_cols:
            self.error_tree.heading(col, text=col)
            self.error_tree.column(col, width=col_widths.get(col, 100), anchor="center" if col in ("#", "Línea", "Columna") else "w")

        err_scroll_y = ttk.Scrollbar(tab_errors, orient=tk.VERTICAL, command=self.error_tree.yview)
        self.error_tree.configure(yscrollcommand=err_scroll_y.set)
        
        self.error_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        err_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña 3: Flujo de Tokens
        tab_tokens = tk.Frame(notebook, bg="#181825")
        notebook.add(tab_tokens, text="  🏷 Flujo de Tokens  ")

        token_cols = ("#", "Línea", "Columna", "Tipo de Token", "Lexema")
        self.token_tree = ttk.Treeview(tab_tokens, columns=token_cols, show="headings", selectmode="browse")
        
        tok_widths = {"#": 50, "Línea": 70, "Columna": 70, "Tipo de Token": 200, "Lexema": 250}
        for col in token_cols:
            self.token_tree.heading(col, text=col)
            self.token_tree.column(col, width=tok_widths.get(col, 120), anchor="center" if col in ("#", "Línea", "Columna") else "w")

        tok_scroll_y = ttk.Scrollbar(tab_tokens, orient=tk.VERTICAL, command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=tok_scroll_y.set)

        self.token_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tok_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_status_bar(self):
        self.status_bar = tk.Label(
            self.root, 
            text="Listo para analizar.", 
            font=("Segoe UI", 9, "bold"), 
            bg="#313244", 
            fg="#cdd6f4", 
            anchor="w", 
            padx=12, 
            pady=4
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _load_selected_suite(self, suite_name: str):
        code = self.TEST_SUITES.get(suite_name, "")
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, code)
        self.analyze_code()

    def _clear_editor(self):
        self.code_editor.delete("1.0", tk.END)
        self.ast_text.delete("1.0", tk.END)
        for row in self.error_tree.get_children():
            self.error_tree.delete(row)
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.status_bar.config(text="Editor limpio.", fg="#cdd6f4")

    def analyze_code(self):
        code = self.code_editor.get("1.0", tk.END)
        
        # Limpiar resultados anteriores
        self.ast_text.delete("1.0", tk.END)
        for row in self.error_tree.get_children():
            self.error_tree.delete(row)
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)

        # 1. Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Cargar tokens en tabla
        for idx, tok in enumerate(tokens, 1):
            self.token_tree.insert("", tk.END, values=(idx, tok.line, tok.column, tok.type.name, tok.value))

        # 2. Parser
        error_handler = SyntaxErrorHandler()
        parser = Parser(tokens, error_handler)
        ast = parser.parse()

        # 3. Mostrar AST
        ast_str = ast.to_tree_str()
        self.ast_text.insert(tk.END, ast_str)

        # 4. Mostrar Errores
        if error_handler.has_errors():
            for idx, err in enumerate(error_handler.errors, 1):
                self.error_tree.insert("", tk.END, values=(
                    idx, err.line, err.column, err.offending_token or "N/A", err.message, err.suggestion
                ))
            self.status_bar.config(
                text=f"❌ Se encontraron {len(error_handler.errors)} errores sintácticos. Revise la pestaña de Errores.",
                fg="#f38ba8"
            )
        else:
            self.status_bar.config(
                text=f"✔ Análisis sintáctico completado exitosamente (0 errores). Árbol AST generado.",
                fg="#a6e3a1"
            )

def main():
    root = tk.Tk()
    app = SyntaxAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
