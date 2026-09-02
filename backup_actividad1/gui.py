"""
================================================================================
ACTIVIDAD 1: DEFINICIÓN DE TOKENS Y EXPRESIONES REGULARES (ANALIZADOR LÉXICO C)
MATERIA: COMPILADORES
PROFESOR: RIGOBERTO CARDENAS LARIOS

INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
1. DIAZ TORRES JAZMIN MONTSERRAT
2. FIERRO MELÉNDEZ ERNESTO HATUEY
3. HERNANDEZ GARCIA HECTOR GABRIEL
4. MILLAN GUERRERO OSWALDO JOSUE
================================================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from lexer import LexerC
from token_type import TokenType
from test_cases import C_VALID_TEST_1, C_VALID_TEST_2, C_INVALID_TEST

class LexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico C - Actividad 1 (Compiladores)")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        # Aplicar estilo visual moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color Palette
        PRIMARY_COLOR = "#1e1e2e"
        ACCENT_COLOR = "#89b4fa"
        BG_COLOR = "#181825"
        TEXT_COLOR = "#cdd6f4"
        
        self.root.configure(bg=BG_COLOR)

        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Cargar caso de prueba por defecto
        self.code_editor.insert(tk.END, C_VALID_TEST_1)
        self.analyze_code()

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e1e2e", padx=15, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame, 
            text="ANALIZADOR LÉXICO PARA LENGUAJE C", 
            font=("Segoe UI", 16, "bold"), 
            bg="#1e1e2e", 
            fg="#89b4fa"
        )
        title_label.pack(anchor="w")

        subtitle = "Integrantes (Orden Alfabético por Primer Apellido):\n" \
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
        # PanedWindow para dividir editor y tabla de tokens
        paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Panel Superior: Editor y Controles
        top_frame = ttk.Frame(paned)
        paned.add(top_frame, weight=1)

        # Barra de botones
        toolbar = ttk.Frame(top_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        btn_analyze = tk.Button(
            toolbar, 
            text="⚡ ANALIZAR CÓDIGO C", 
            font=("Segoe UI", 10, "bold"),
            bg="#a6e3a1", 
            fg="#11111b", 
            padx=12, 
            pady=4,
            relief=tk.FLAT,
            command=self.analyze_code
        )
        btn_analyze.pack(side=tk.LEFT, padx=(0, 5))

        btn_test1 = ttk.Button(toolbar, text="Cargar Prueba 1 (Válida)", command=lambda: self.load_test(C_VALID_TEST_1))
        btn_test1.pack(side=tk.LEFT, padx=3)

        btn_test2 = ttk.Button(toolbar, text="Cargar Prueba 2 (Válida)", command=lambda: self.load_test(C_VALID_TEST_2))
        btn_test2.pack(side=tk.LEFT, padx=3)

        btn_test_inv = ttk.Button(toolbar, text="Cargar Prueba 3 (Errores)", command=lambda: self.load_test(C_INVALID_TEST))
        btn_test_inv.pack(side=tk.LEFT, padx=3)

        btn_clear = ttk.Button(toolbar, text="Limpiar", command=self.clear_editor)
        btn_clear.pack(side=tk.RIGHT, padx=3)

        # Area de Texto Código C
        editor_label = tk.Label(top_frame, text="Código Fuente en Lenguaje C:", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#181825")
        editor_label.pack(anchor="w")

        self.code_editor = scrolledtext.ScrolledText(
            top_frame, 
            font=("Consolas", 11), 
            bg="#1e1e2e", 
            fg="#cdd6f4",
            insertbackground="white",
            height=10
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Panel Inferior: Tabla de Tokens Resultante
        bottom_frame = ttk.Frame(paned)
        paned.add(bottom_frame, weight=2)

        table_label = tk.Label(bottom_frame, text="Componentes Léxicos Identificados (Tabla de Tokens):", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#181825")
        table_label.pack(anchor="w", pady=(5, 2))

        # Treeview (Tabla)
        columns = ("num", "line", "col", "type", "lexeme", "status")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings", height=12)

        self.tree.heading("num", text="#")
        self.tree.heading("line", text="Línea")
        self.tree.heading("col", text="Columna")
        self.tree.heading("type", text="Categoría Léxica")
        self.tree.heading("lexeme", text="Lexema / Valor")
        self.tree.heading("status", text="Estado")

        self.tree.column("num", width=40, anchor="center")
        self.tree.column("line", width=60, anchor="center")
        self.tree.column("col", width=65, anchor="center")
        self.tree.column("type", width=180, anchor="w")
        self.tree.column("lexeme", width=380, anchor="w")
        self.tree.column("status", width=120, anchor="center")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar colores de filas según estado
        self.tree.tag_configure("valid", foreground="#11111b", background="#e6e9ef")
        self.tree.tag_configure("error", foreground="#ffffff", background="#f38ba8")
        self.tree.tag_configure("keyword", foreground="#000000", background="#cba6f7")
        self.tree.tag_configure("comment", foreground="#45475a", background="#f5e0dc")

    def _create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg="#11111b", padx=15, pady=5)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(
            self.status_frame, 
            text="Listo para analizar.", 
            font=("Segoe UI", 10, "bold"), 
            bg="#11111b", 
            fg="#a6e3a1"
        )
        self.status_label.pack(side=tk.LEFT)

    def load_test(self, test_code: str):
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, test_code)
        self.analyze_code()

    def clear_editor(self):
        self.code_editor.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())
        self.status_label.config(text="Editor limpiado.", fg="#cdd6f4")

    def analyze_code(self):
        code = self.code_editor.get("1.0", tk.END)
        lexer = LexerC(code)
        tokens = lexer.tokenize()

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        valid_count = 0
        error_count = 0

        for idx, token in enumerate(tokens, 1):
            lex_display = repr(token.value)[1:-1] if '\n' in token.value or '\t' in token.value else token.value
            
            if token.type == TokenType.ERROR_LEXICO:
                status = "ERROR LÉXICO"
                tag = "error"
                error_count += 1
            else:
                status = "VÁLIDO"
                if token.type == TokenType.PALABRA_CLAVE:
                    tag = "keyword"
                elif token.type in (TokenType.COMENTARIO_LINEA, TokenType.COMENTARIO_BLOQUE):
                    tag = "comment"
                else:
                    tag = "valid"
                valid_count += 1

            self.tree.insert("", tk.END, values=(idx, token.line, token.column, token.type.value, lex_display, status), tags=(tag,))

        if error_count == 0:
            self.status_label.config(text=f"✔ Análisis Completado: {valid_count} Tokens Reconocidos Correctamente sin Errores.", fg="#a6e3a1")
        else:
            self.status_label.config(text=f"⚠ Análisis Completado: {valid_count} Tokens Reconocidos | {error_count} Errores Léxicos Encontrados.", fg="#f38ba8")

def main():
    root = tk.Tk()
    app = LexerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
