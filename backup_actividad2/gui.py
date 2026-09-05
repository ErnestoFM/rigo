"""
================================================================================
ACTIVIDAD 2: MANEJO DE ERRORES LÉXICOS (COMPILADOR LENGUAJE C EN PYTHON)
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
from lexer import LexerC
from token_type import TokenType
from test_cases import (
    C_VALID_TEST,
    C_TEST_UNRECOGNIZED_CHARS,
    C_TEST_MALFORMED_IDENTIFIERS,
    C_TEST_INCORRECT_NUMBERS,
    C_TEST_UNCLOSED_STRINGS,
    C_TEST_COMBINED_ERRORS
)

class LexerGUIActividad2:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador C - Actividad 2: Gestión de Errores Léxicos")
        self.root.geometry("1150x800")
        self.root.minsize(950, 650)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        BG_COLOR = "#181825"
        self.root.configure(bg=BG_COLOR)

        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Cargar caso combinado por defecto
        self.code_editor.insert(tk.END, C_TEST_COMBINED_ERRORS)
        self.analyze_code()

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e1e2e", padx=15, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame, 
            text="ANALIZADOR LÉXICO C - MANEJO DE ERRORES LÉXICOS", 
            font=("Segoe UI", 15, "bold"), 
            bg="#1e1e2e", 
            fg="#f38ba8"
        )
        title_label.pack(anchor="w")

        subtitle = "Integrantes del Equipo (Orden Alfabético por Primer Apellido):\n" \
                   "1. DIAZ TORRES JAZMIN MONTSERRAT | 2. FIERRO MELÉNDEZ ERNESTO HATUEY\n" \
                   "3. HERNANDEZ GARCIA HECTOR GABRIEL | 4. MILLAN GUERRERO OSWALDO JOSUE"
        
        members_label = tk.Label(
            header_frame, 
            text=subtitle, 
            font=("Segoe UI", 9), 
            bg="#1e1e2e", 
            fg="#a6adc8",
            justify=tk.LEFT
        )
        members_label.pack(anchor="w", pady=(2, 0))

    def _create_main_content(self):
        paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Panel Superior: Editor de Código C y Botones de Prueba
        top_frame = ttk.Frame(paned)
        paned.add(top_frame, weight=1)

        toolbar = ttk.Frame(top_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        btn_analyze = tk.Button(
            toolbar, 
            text="⚡ ANALIZAR Y GESTIONAR ERRORES", 
            font=("Segoe UI", 10, "bold"),
            bg="#f38ba8", 
            fg="#11111b", 
            padx=12, 
            pady=4,
            relief=tk.FLAT,
            command=self.analyze_code
        )
        btn_analyze.pack(side=tk.LEFT, padx=(0, 5))

        btn_t1 = ttk.Button(toolbar, text="1. Caracteres Exóticos", command=lambda: self.load_test(C_TEST_UNRECOGNIZED_CHARS))
        btn_t1.pack(side=tk.LEFT, padx=2)

        btn_t2 = ttk.Button(toolbar, text="2. Identificadores Malos", command=lambda: self.load_test(C_TEST_MALFORMED_IDENTIFIERS))
        btn_t2.pack(side=tk.LEFT, padx=2)

        btn_t3 = ttk.Button(toolbar, text="3. Números Malos", command=lambda: self.load_test(C_TEST_INCORRECT_NUMBERS))
        btn_t3.pack(side=tk.LEFT, padx=2)

        btn_t4 = ttk.Button(toolbar, text="4. Cadenas Sin Cerrar", command=lambda: self.load_test(C_TEST_UNCLOSED_STRINGS))
        btn_t4.pack(side=tk.LEFT, padx=2)

        btn_t5 = ttk.Button(toolbar, text="5. Caso Combinado", command=lambda: self.load_test(C_TEST_COMBINED_ERRORS))
        btn_t5.pack(side=tk.LEFT, padx=2)

        btn_valid = ttk.Button(toolbar, text="✔ Código Válido", command=lambda: self.load_test(C_VALID_TEST))
        btn_valid.pack(side=tk.LEFT, padx=2)

        # Editor de Texto
        editor_label = tk.Label(top_frame, text="Código Fuente C a Diagnosticar:", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#181825")
        editor_label.pack(anchor="w")

        self.code_editor = scrolledtext.ScrolledText(
            top_frame, 
            font=("Consolas", 11), 
            bg="#1e1e2e", 
            fg="#cdd6f4",
            insertbackground="white",
            height=9
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Panel Inferior: Pestañas para Resultados de Tokens y Reporte de Errores
        bottom_frame = ttk.Frame(paned)
        paned.add(bottom_frame, weight=2)

        self.notebook = ttk.Notebook(bottom_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Tabla Completa de Tokens
        tab_tokens = ttk.Frame(self.notebook)
        self.notebook.add(tab_tokens, text=" 📋 Tabla General de Tokens ")

        cols_tokens = ("num", "line", "col", "type", "lexeme", "status")
        self.tree_tokens = ttk.Treeview(tab_tokens, columns=cols_tokens, show="headings", height=10)
        self.tree_tokens.heading("num", text="#")
        self.tree_tokens.heading("line", text="Línea")
        self.tree_tokens.heading("col", text="Columna")
        self.tree_tokens.heading("type", text="Categoría Léxica")
        self.tree_tokens.heading("lexeme", text="Lexema / Valor")
        self.tree_tokens.heading("status", text="Estado")

        self.tree_tokens.column("num", width=40, anchor="center")
        self.tree_tokens.column("line", width=60, anchor="center")
        self.tree_tokens.column("col", width=65, anchor="center")
        self.tree_tokens.column("type", width=220, anchor="w")
        self.tree_tokens.column("lexeme", width=380, anchor="w")
        self.tree_tokens.column("status", width=140, anchor="center")

        scroll_tok = ttk.Scrollbar(tab_tokens, orient=tk.VERTICAL, command=self.tree_tokens.yview)
        self.tree_tokens.configure(yscrollcommand=scroll_tok.set)
        self.tree_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tok.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña 2: Panel Exclusivo de Errores Léxicos
        tab_errors = ttk.Frame(self.notebook)
        self.notebook.add(tab_errors, text=" ⚠️ Diagnóstico de Errores Léxicos ")

        cols_err = ("num", "line", "col", "cat", "lexeme", "desc", "sug")
        self.tree_errors = ttk.Treeview(tab_errors, columns=cols_err, show="headings", height=10)
        self.tree_errors.heading("num", text="#")
        self.tree_errors.heading("line", text="Línea")
        self.tree_errors.heading("col", text="Col")
        self.tree_errors.heading("cat", text="Tipo de Error Léxico")
        self.tree_errors.heading("lexeme", text="Lexema Erróneo")
        self.tree_errors.heading("desc", text="Descripción del Problema")
        self.tree_errors.heading("sug", text="Sugerencia de Corrección")

        self.tree_errors.column("num", width=35, anchor="center")
        self.tree_errors.column("line", width=55, anchor="center")
        self.tree_errors.column("col", width=45, anchor="center")
        self.tree_errors.column("cat", width=190, anchor="w")
        self.tree_errors.column("lexeme", width=140, anchor="w")
        self.tree_errors.column("desc", width=260, anchor="w")
        self.tree_errors.column("sug", width=260, anchor="w")

        scroll_err = ttk.Scrollbar(tab_errors, orient=tk.VERTICAL, command=self.tree_errors.yview)
        self.tree_errors.configure(yscrollcommand=scroll_err.set)
        self.tree_errors.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_err.pack(side=tk.RIGHT, fill=tk.Y)

        # Estilos de filas
        self.tree_tokens.tag_configure("valid", foreground="#11111b", background="#e6e9ef")
        self.tree_tokens.tag_configure("error", foreground="#ffffff", background="#f38ba8")
        self.tree_errors.tag_configure("error_row", foreground="#ffffff", background="#e78284")

    def _create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg="#11111b", padx=15, pady=6)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(
            self.status_frame, 
            text="Listo para analizar.", 
            font=("Segoe UI", 10, "bold"), 
            bg="#11111b", 
            fg="#a6e3a1"
        )
        self.status_label.pack(side=tk.LEFT)

    def load_test(self, code: str):
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, code)
        self.analyze_code()

    def analyze_code(self):
        code = self.code_editor.get("1.0", tk.END)
        lexer = LexerC(code)
        tokens = lexer.tokenize()

        # Limpiar ambas tablas
        for item in self.tree_tokens.get_children():
            self.tree_tokens.delete(item)
        for item in self.tree_errors.get_children():
            self.tree_errors.delete(item)

        valid_count = 0
        error_count = 0

        for idx, token in enumerate(tokens, 1):
            lex_display = repr(token.value)[1:-1] if '\n' in token.value or '\t' in token.value else token.value
            
            if token.is_error:
                status = "ERROR LÉXICO"
                tag = "error"
                error_count += 1
            else:
                status = "VÁLIDO"
                tag = "valid"
                valid_count += 1

            self.tree_tokens.insert("", tk.END, values=(idx, token.line, token.column, token.type.value, lex_display, status), tags=(tag,))

        # Llenar la tabla de Errores Léxicos
        for idx, err in enumerate(lexer.error_handler.errors, 1):
            lex_display = repr(err.lexeme)[1:-1] if '\n' in err.lexeme or '\t' in err.lexeme else err.lexeme
            self.tree_errors.insert(
                "", tk.END, 
                values=(idx, err.line, err.column, err.category.value, lex_display, err.description, err.suggestion),
                tags=("error_row",)
            )

        if error_count == 0:
            self.status_label.config(text=f"✔ Análisis Léxico Limpio: {valid_count} Tokens Reconocidos | 0 Errores Léxicos.", fg="#a6e3a1")
            self.notebook.select(0)
        else:
            self.status_label.config(text=f"⚠ Se Detectaron {error_count} Errores Léxicos. Consulte la pestaña de Diagnóstico.", fg="#f38ba8")
            self.notebook.select(1)

def main():
    root = tk.Tk()
    app = LexerGUIActividad2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
