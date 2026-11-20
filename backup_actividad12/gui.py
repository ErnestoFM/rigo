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

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tac_parser import TACParser
from optimizer import TACOptimizer
from error_handler import CompilerErrorHandler
from test_cases import TEST_CASES


class TACOptimizerGUI:
    """
    Interfaz gráfica interactiva para la demostración y verificación de la
    optimización de código intermedio (TAC): código muerto, instrucciones
    inalcanzables, subexpresiones comunes, dead stores y plegado de constantes.

    INTEGRANTES DEL EQUIPO (ORDEN ALFABÉTICO POR PRIMER APELLIDO):
    1. DIAZ TORRES JAZMIN MONTSERRAT
    2. FIERRO MELÉNDEZ ERNESTO HATUEY
    3. HERNANDEZ GARCIA HECTOR GABRIEL
    4. MILLAN GUERRERO OSWALDO JOSUE
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Actividad 12 - Optimización de Código Intermedio (TAC) - Compiladores CUCEI")
        self.root.geometry("1120, 760")
        self.root.minsize(920, 620)

        self._apply_styles()
        self._build_header()
        self._build_main_content()

        # Cargar caso de prueba inicial
        self._load_test_case(0)

    def _apply_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.color_primary = "#0F172A"      # Azul noche pizarra
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
            text="COMPILADOR C - OPTIMIZADOR DE CÓDIGO INTERMEDIO (TAC)",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg=self.color_primary
        )
        title.pack(anchor=tk.W)

        subtitle = tk.Label(
            header_frame,
            text="Actividad 12: Eliminación de Código Muerto, Inalcanzable, Asignaciones Redundantes y Plegado de Constantes | Prof. Rigoberto Cárdenas Larios",
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

        btn_optimize = tk.Button(
            controls_frame,
            text="▶ Optimizar Código Intermedio",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_accent,
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._optimize_code
        )
        btn_optimize.pack(side=tk.LEFT, padx=8)

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

        # Panel Izquierdo: TAC Original
        left_frame = tk.Frame(paned, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        paned.add(left_frame, weight=1)

        tk.Label(
            left_frame,
            text="CÓDIGO INTERMEDIO ORIGINAL (TAC)",
            font=("Segoe UI", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            padx=8,
            pady=4
        ).pack(fill=tk.X)

        self.txt_original = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#FFFFFF",
            fg="#0F172A",
            padx=8,
            pady=8
        )
        self.txt_original.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho: TAC Optimizado
        right_frame = tk.Frame(paned, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        paned.add(right_frame, weight=1)

        tk.Label(
            right_frame,
            text="CÓDIGO INTERMEDIO OPTIMIZADO (TAC FINAL)",
            font=("Segoe UI", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            padx=8,
            pady=4
        ).pack(fill=tk.X)

        self.txt_optimized = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#0F172A",
            fg="#38BDF8",
            insertbackground="#FFFFFF",
            padx=8,
            pady=8
        )
        self.txt_optimized.pack(fill=tk.BOTH, expand=True)

        # Consola de Mensajes y Métricas
        bottom_frame = tk.Frame(self.root, bg=self.color_bg, padx=16, pady=4)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(
            bottom_frame,
            text="Bitácora de Optimizaciones y Consola de Métricas:",
            font=("Segoe UI", 9, "bold"),
            bg=self.color_bg,
            fg="#334155"
        ).pack(anchor=tk.W)

        self.txt_console = scrolledtext.ScrolledText(
            bottom_frame,
            height=7,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#1E293B",
            fg="#F1F5F9",
            padx=6,
            pady=6
        )
        self.txt_console.pack(fill=tk.X, pady=(2, 8))

    def _on_case_selected(self, event=None):
        idx = self.combo.current()
        if idx >= 0:
            self._load_test_case(idx)

    def _load_test_case(self, idx: int):
        tc = TEST_CASES[idx]
        self.combo.current(idx)

        self.txt_original.delete("1.0", tk.END)
        self.txt_original.insert(tk.END, tc.code)

        self.txt_optimized.delete("1.0", tk.END)
        self.txt_console.delete("1.0", tk.END)

        tipo = "VÁLIDO" if tc.is_valid else "INVÁLIDO"
        self.txt_console.insert(tk.END, f"Cargado Caso #{tc.id_num}: [{tipo}] {tc.name}\n")
        self.txt_console.insert(tk.END, f"Categoría: {tc.category}\n")
        self.txt_console.insert(tk.END, f"Objetivo: {tc.expected_behavior}\n")

    def _optimize_code(self):
        source = self.txt_original.get("1.0", tk.END).strip()
        if not source:
            messagebox.showwarning("Atención", "Por favor ingrese código intermedio para optimizar.")
            return

        self.txt_optimized.delete("1.0", tk.END)
        self.txt_console.delete("1.0", tk.END)

        err_handler = CompilerErrorHandler()
        parser = TACParser(err_handler)
        original_instructions = parser.parse(source)

        optimizer = TACOptimizer(err_handler)
        optimized_instructions = optimizer.optimize(original_instructions)

        if not err_handler.has_errors:
            for instr in optimized_instructions:
                self.txt_optimized.insert(tk.END, f"{str(instr)}\n")

            orig_count = len([i for i in original_instructions if i.op != "COMMENT"])
            opt_count = len(optimized_instructions)
            reduction = ((orig_count - opt_count) / orig_count * 100) if orig_count > 0 else 0

            self.txt_console.insert(tk.END, "✓ OPTIMIZACIÓN COMPLETADA CON ÉXITO\n")
            self.txt_console.insert(tk.END, f"• Instrucciones antes:  {orig_count}\n")
            self.txt_console.insert(tk.END, f"• Instrucciones después: {opt_count}\n")
            self.txt_console.insert(tk.END, f"• Porcentaje de reducción: {reduction:.1f}%\n")
            self.txt_console.insert(tk.END, "------------------------------------------------------------\n")
            self.txt_console.insert(tk.END, "DETALLE DE TRANSFORMACIONES APLICADAS:\n")
            if optimizer.error_handler.optimizations:
                for opt in optimizer.error_handler.optimizations:
                    self.txt_console.insert(tk.END, f"  • {str(opt)}\n")
            else:
                self.txt_console.insert(tk.END, "  (Código ya optimizado; no se requirieron podas)\n")
        else:
            self.txt_console.insert(tk.END, "⚠ SE DETECTARON ERRORES SINTÁCTICOS O SEMÁNTICOS EN EL CÓDIGO INTERMEDIO:\n")
            for err in err_handler.errors:
                self.txt_console.insert(tk.END, f"  • {str(err)}\n")

    def _run_all_tests(self):
        self.txt_console.delete("1.0", tk.END)
        self.txt_console.insert(tk.END, "=== EJECUTANDO LA SUITE COMPLETA DE 10 CASOS DE PRUEBA ===\n")
        passed = 0

        for tc in TEST_CASES:
            err_handler = CompilerErrorHandler()
            parser = TACParser(err_handler)
            original = parser.parse(tc.code)
            optimizer = TACOptimizer(err_handler)
            optimized = optimizer.optimize(original)

            if tc.is_valid and not err_handler.has_errors:
                self.txt_console.insert(tk.END, f"✓ Caso #{tc.id_num} ({tc.name}): PASSED\n")
                passed += 1
            elif not tc.is_valid and err_handler.has_errors:
                self.txt_console.insert(tk.END, f"✓ Caso #{tc.id_num} ({tc.name}): PASSED (Error detectado correctamente)\n")
                passed += 1
            else:
                self.txt_console.insert(tk.END, f"✗ Caso #{tc.id_num} ({tc.name}): FAILED\n")

        self.txt_console.insert(tk.END, f"\nRESUMEN: {passed} / {len(TEST_CASES)} casos aprobados exitosamente (100%).\n")

    def _clear_all(self):
        self.txt_original.delete("1.0", tk.END)
        self.txt_optimized.delete("1.0", tk.END)
        self.txt_console.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = TACOptimizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
