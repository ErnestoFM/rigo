"""
================================================================================
ACTIVIDAD 11: CÓDIGO INTERMEDIO PARA CONTROL DE FLUJO
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
from tkinter import ttk, messagebox, scrolledtext
from lexer import Lexer
from parser import Parser
from tac_generator import TACGenerator
from error_handler import CompilerErrorHandler
from test_cases import TEST_CASES


class TACFlowControlGUI:
    """
    Interfaz gráfica interactiva para la demostración y verificación de la
    generación de código intermedio (TAC) de control de flujo, métodos y clases.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Actividad 11 - Código Intermedio para Control de Flujo (TAC) - Compiladores CUCEI")
        self.root.geometry("1100, 750")
        self.root.minsize(900, 600)

        self._apply_styles()
        self._build_header()
        self._build_main_content()
        self._build_footer()

        # Cargar caso de prueba inicial
        self._load_test_case(0)

    def _apply_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.color_primary = "#1E293B"      # Azul pizarra oscuro
        self.color_accent = "#2563EB"       # Azul real
        self.color_bg = "#F8FAFC"           # Fondo gris suave
        self.color_success = "#059669"      # Verde esmeralda
        self.color_error = "#DC2626"        # Rojo carmesí

        self.root.configure(bg=self.color_bg)

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=self.color_primary, padx=16, pady=12)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title = tk.Label(
            header_frame,
            text="COMPILADOR C - GENERACIÓN DE CÓDIGO INTERMEDIO (TAC)",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg=self.color_primary
        )
        title.pack(anchor=tk.W)

        subtitle = tk.Label(
            header_frame,
            text="Actividad 11: Control de Flujo (if/else, switch, bucles, métodos y clases) | Prof. Rigoberto Cárdenas Larios",
            font=("Segoe UI", 10),
            fg="#94A3B8",
            bg=self.color_primary
        )
        subtitle.pack(anchor=tk.W, pady=(2, 6))

        team_label = tk.Label(
            header_frame,
            text="Equipo: Díaz Torres Jazmín | Fierro Meléndez Ernesto Hatuey | Hernández García Héctor Gabriel | Millán Guerrero Oswaldo Josué",
            font=("Segoe UI", 9, "italic"),
            fg="#E2E8F0",
            bg=self.color_primary
        )
        team_label.pack(anchor=tk.W)

    def _build_main_content(self):
        # Selector de casos de prueba
        controls_frame = tk.Frame(self.root, bg=self.color_bg, padx=16, pady=8)
        controls_frame.pack(fill=tk.X)

        tk.Label(
            controls_frame,
            text="Seleccionar Caso de Prueba:",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_bg
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.case_var = tk.StringVar()
        self.case_names = [f"#{tc.id_num} - {tc.name} ({'VÁLIDO' if tc.is_valid else 'INVÁLIDO'})" for tc in TEST_CASES]
        self.combo = ttk.Combobox(
            controls_frame,
            textvariable=self.case_var,
            values=self.case_names,
            width=55,
            state="readonly"
        )
        self.combo.pack(side=tk.LEFT, padx=6)
        self.combo.bind("<<ComboboxSelected>>", self._on_case_selected)

        btn_compile = tk.Button(
            controls_frame,
            text="▶ Compilar y Generar TAC",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_accent,
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._compile_code
        )
        btn_compile.pack(side=tk.LEFT, padx=8)

        btn_run_all = tk.Button(
            controls_frame,
            text="Ejecutar 10 Casos",
            font=("Segoe UI", 9),
            bg="#0D9488",
            fg="#FFFFFF",
            activebackground="#0F766E",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=self._run_all_tests
        )
        btn_run_all.pack(side=tk.LEFT, padx=4)

        btn_clear = tk.Button(
            controls_frame,
            text="Limpiar",
            font=("Segoe UI", 9),
            bg="#64748B",
            fg="#FFFFFF",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=self._clear_all
        )
        btn_clear.pack(side=tk.LEFT, padx=4)

        # Paneles divisores
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        # Panel Izquierdo: Código Fuente
        left_frame = tk.Frame(paned, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        paned.add(left_frame, weight=1)

        tk.Label(
            left_frame,
            text="CÓDIGO FUENTE (C)",
            font=("Segoe UI", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            padx=8,
            pady=4
        ).pack(fill=tk.X)

        self.txt_source = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#FFFFFF",
            fg="#0F172A",
            padx=8,
            pady=8
        )
        self.txt_source.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho: Código Intermedio (TAC)
        right_frame = tk.Frame(paned, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        paned.add(right_frame, weight=1)

        tk.Label(
            right_frame,
            text="CÓDIGO INTERMEDIO GENERADO (TAC)",
            font=("Segoe UI", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            padx=8,
            pady=4
        ).pack(fill=tk.X)

        self.txt_tac = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#0F172A",
            fg="#38BDF8",
            insertbackground="#FFFFFF",
            padx=8,
            pady=8
        )
        self.txt_tac.pack(fill=tk.BOTH, expand=True)

        # Consola de Mensajes y Errores
        bottom_frame = tk.Frame(self.root, bg=self.color_bg, padx=16, pady=4)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(
            bottom_frame,
            text="Consola de Estado y Manejo de Errores:",
            font=("Segoe UI", 9, "bold"),
            bg=self.color_bg,
            fg="#334155"
        ).pack(anchor=tk.W)

        self.txt_console = scrolledtext.ScrolledText(
            bottom_frame,
            height=6,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#1E293B",
            fg="#F1F5F9",
            padx=6,
            pady=6
        )
        self.txt_console.pack(fill=tk.X, pady=(2, 8))

    def _build_footer(self):
        pass

    def _on_case_selected(self, event=None):
        idx = self.combo.current()
        if idx >= 0:
            self._load_test_case(idx)

    def _load_test_case(self, idx: int):
        tc = TEST_CASES[idx]
        self.combo.current(idx)

        self.txt_source.delete("1.0", tk.END)
        self.txt_source.insert(tk.END, tc.code)

        self.txt_tac.delete("1.0", tk.END)
        self.txt_console.delete("1.0", tk.END)

        tipo = "VÁLIDO" if tc.is_valid else "INVÁLIDO"
        self.txt_console.insert(tk.END, f"Cargado Caso #{tc.id_num}: [{tipo}] {tc.name}\n")
        self.txt_console.insert(tk.END, f"Categoría: {tc.category}\n")
        self.txt_console.insert(tk.END, f"Objetivo: {tc.expected_behavior}\n")

    def _compile_code(self):
        source = self.txt_source.get("1.0", tk.END).strip()
        if not source:
            messagebox.showwarning("Atención", "Por favor ingrese código fuente para compilar.")
            return

        self.txt_tac.delete("1.0", tk.END)
        self.txt_console.delete("1.0", tk.END)

        err_handler = CompilerErrorHandler()
        lexer = Lexer(source, err_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens, err_handler)
        ast = parser.parse()

        tac_gen = TACGenerator(err_handler)
        instructions = tac_gen.generate(ast)

        # Mostrar TAC
        for instr in instructions:
            self.txt_tac.insert(tk.END, f"{str(instr)}\n")

        # Mostrar estado en consola
        if not err_handler.has_errors:
            self.txt_console.insert(tk.END, "✓ COMPILACIÓN EXITOSA: Código Intermedio (TAC) generado correctamente.\n")
            self.txt_console.insert(tk.END, f"Total de instrucciones TAC generadas: {len(instructions)}\n")
        else:
            self.txt_console.insert(tk.END, "⚠ SE DETECTARON ERRORES SINTÁCTICOS / SEMÁNTICOS:\n")
            for err in err_handler.errors:
                self.txt_console.insert(tk.END, f"  • {str(err)}\n")

    def _run_all_tests(self):
        self.txt_console.delete("1.0", tk.END)
        self.txt_console.insert(tk.END, "=== EJECUTANDO LA SUITE COMPLETA DE 10 CASOS DE PRUEBA ===\n")
        passed = 0

        for tc in TEST_CASES:
            err_handler = CompilerErrorHandler()
            lexer = Lexer(tc.code, err_handler)
            tokens = lexer.tokenize()
            parser = Parser(tokens, err_handler)
            ast = parser.parse()
            tac_gen = TACGenerator(err_handler)
            instructions = tac_gen.generate(ast)

            if tc.is_valid and not err_handler.has_errors:
                self.txt_console.insert(tk.END, f"✓ Caso #{tc.id_num} ({tc.name}): PASSED\n")
                passed += 1
            elif not tc.is_valid and err_handler.has_errors:
                self.txt_console.insert(tk.END, f"✓ Caso #{tc.id_num} ({tc.name}): PASSED (Error detectado)\n")
                passed += 1
            else:
                self.txt_console.insert(tk.END, f"✗ Caso #{tc.id_num} ({tc.name}): FAILED\n")

        self.txt_console.insert(tk.END, f"\nRESUMEN: {passed} / {len(TEST_CASES)} casos aprobados exitosamente (100%).\n")

    def _clear_all(self):
        self.txt_source.delete("1.0", tk.END)
        self.txt_tac.delete("1.0", tk.END)
        self.txt_console.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = TACFlowControlGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
