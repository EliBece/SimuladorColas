# MIT License
# Copyright (c) 2025 Elizabeth Becerril y Sofía Becerril
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ====================================================================================================
# INTERFAZ [MODELO MM1 - MMc MARKOVIANO]
# ====================================================================================================

import os
import sys
from PIL import Image
import customtkinter as ctk
from customtkinter import CTkImage
from matplotlib.figure import Figure
import tkinter.messagebox as messagebox
from utils import mm1_metrics, mmc_metrics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ====================================================================================================
# CONFIGURAR TEMA PREDETERMINADO 
# ====================================================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ====================================================================================================
# CONFIGURAR RUTAS PARA IMAGENES
# ====================================================================================================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if getattr(sys, 'frozen', False):
    ruta_imagen = resource_path(os.path.join("images", "funny_image.png"))
else:
    ruta_imagen = resource_path(os.path.join("..", "images", "funny_image.png"))

# ====================================================================================================
# CONFIGURAR INTERFAZ EN TKINTER
# ====================================================================================================
class SimuladorColas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Ventana Principal ------
        self.title("Simulador de Teoría de Colas Markoviano")
        self.geometry("1200x700")
        self.state("zoomed")

        # --- Variables Predeterminadas ------
        self.modelo_var = ctk.StringVar(value="")
        self.modelo_var.trace_add("write", self.actualizar_campos)
        self.unidad_tiempo_var = ctk.StringVar(value="")
        
        # --- Contenedor Principal -------
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # --- Panel Izq Entradas -----
        self.panel_izquierdo = ctk.CTkFrame(self)
        self.panel_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # --- Panel Der Resultados -----
        self.panel_derecho = ctk.CTkFrame(self)
        self.panel_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self._crear_panel_inputs()
        self._crear_panel_resultados()

        # --- Mostrar Imagen -----
        imagen = Image.open(ruta_imagen)
        imagen_resized = imagen.resize((200, 200))  
        self.imagen_graciosa = CTkImage(light_image=imagen_resized, dark_image=imagen_resized, size=(200, 200))

        self.label_imagen = ctk.CTkLabel(self.panel_izquierdo, image=self.imagen_graciosa, text="")
        self.label_imagen.pack(pady=10)


    # Funciones
    # -----------------------------------------------------------------------------------------------
    # _crear_panel_inputs: Crea y organiza todos los campos de entrada en la interfaz.
    def _crear_panel_inputs(self):
        titulo = ctk.CTkLabel(self.panel_izquierdo, text="Simulador de Teoría de Colas Markoviano", font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=20, padx=20)

        frame_config = ctk.CTkFrame(self.panel_izquierdo, corner_radius=10)
        frame_config.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_config, text="Configuración Inicial", anchor="w", font=ctk.CTkFont(size=18, weight="bold")).pack(fill="x", padx=10, pady=(10, 15))

        opciones_grid = ctk.CTkFrame(frame_config, fg_color="transparent")
        opciones_grid.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(opciones_grid, text="Modelo:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(opciones_grid, text="MM1", variable=self.modelo_var, value="MM1").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(opciones_grid, text="MMc", variable=self.modelo_var, value="MMc").grid(row=0, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(opciones_grid, text="Unidad de tiempo:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(opciones_grid, text="Horas", variable=self.unidad_tiempo_var, value="horas").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(opciones_grid, text="Minutos", variable=self.unidad_tiempo_var, value="minutos").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(opciones_grid, text="").grid(row=2, column=0, pady=3)

        self.frame_entradas = ctk.CTkFrame(self.panel_izquierdo, corner_radius=10)
        self.frame_entradas.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.frame_entradas, text="Ingresa los Datos del Modelo", anchor="w", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 15))

        self.lambda_label, self.lambda_entry = self._crear_entrada(self.frame_entradas, "Tasa de llegada (λ):", row=1)
        self.mu_label, self.mu_entry = self._crear_entrada(self.frame_entradas, "Tasa de servicio (μ):", row=2)
        self.n_label, self.n_entry = self._crear_entrada(self.frame_entradas, "Probabilidades n-ésimas:", row=3)
        self.s_label, self.s_entry = self._crear_entrada(self.frame_entradas, "Número de servidores (c):", row=4)
        ctk.CTkLabel(self.frame_entradas, text="").grid(row=5, column=0, columnspan=2, pady=3)

        self.s_label.grid_remove()
        self.s_entry.grid_remove()

        self.boton_calcular = ctk.CTkButton (
            self.panel_izquierdo,
            text="¿Listo para calcular?",
            command=self.calcular,
            font=ctk.CTkFont(size=16),
            height=45,
            width=250,  
            fg_color="#1f6aa5",
            hover_color="#144e75",
            corner_radius=8
        )
        self.boton_calcular.pack(pady=20)

    # _crear_entrada: Crea un campo de entrada con su etiqueta (Label + Entry) y lo posiciona en el grid.
    def _crear_entrada(self, parent, label_text, row):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14))
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        entry = ctk.CTkEntry(parent, width=250)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        return (label, entry)

     # _actualizar_campos: Muestra u oculta el campo "número de servidores (s)" según el modelo elegido (MM1 o MMS).
    def actualizar_campos(self, *args):
        modelo = self.modelo_var.get()

        if modelo == "MMc":
            self.s_label.grid()
            self.s_entry.grid()
        else:
            self.s_label.grid_remove()
            self.s_entry.grid_remove()

    # _crear_panel_resultados: Crea y organiza el espacio donde se muestran los resultados.
    def _crear_panel_resultados(self):
        self.scrollable_frame_resultados = ctk.CTkScrollableFrame(self.panel_derecho)
        self.scrollable_frame_resultados.pack(padx=20, pady=20, fill="both", expand=True)

        titulo_metricas = ctk.CTkLabel(self.scrollable_frame_resultados, text="Métricas Clave", font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
        titulo_metricas.pack(padx=10, pady=10, fill="x")

        self.labels_resultados = {
            "rho": self._crear_label_resultado(self.scrollable_frame_resultados, "Factor de uso (ρ):"),
            "Ls": self._crear_label_resultado(self.scrollable_frame_resultados, "Clientes esperados en el sistema (Ls):"),
            "Lq": self._crear_label_resultado(self.scrollable_frame_resultados, "Clientes esperados en la cola (Lq):"),
            "Ws": self._crear_label_resultado(self.scrollable_frame_resultados, "Tiempo esperado en el sistema (Ws):"),
            "Wq": self._crear_label_resultado(self.scrollable_frame_resultados, "Tiempo esperado en la cola (Wq):"),
            "P0": self._crear_label_resultado(self.scrollable_frame_resultados, "Probabilidad del sistema vacío (P₀):")
        }
        ctk.CTkFrame(self.scrollable_frame_resultados, height=20, fg_color="transparent").pack()

        frame_prob = ctk.CTkFrame(self.scrollable_frame_resultados, corner_radius=10)
        frame_prob.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(frame_prob, text="Probabilidades n-ésimas (Pₙ)", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(padx=10, pady=5, fill="x")

        self.prob_text = ctk.CTkTextbox(frame_prob, height=150, font=ctk.CTkFont(size=14))
        self.prob_text.pack(padx=10, pady=5, fill="x")
        self.prob_text.configure(state="disabled")
        ctk.CTkFrame(frame_prob, height=10, fg_color="transparent").pack()

        self.frame_grafica = ctk.CTkFrame(self.scrollable_frame_resultados, corner_radius=10)
        self.frame_grafica.pack(padx=10, pady=10, fill="both", expand=True)

    # _crear_label_resultado: Crea una fila para mostrar el nombre y valor de cada métrica.
    def _crear_label_resultado(self, parent, texto):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=10, pady=5)

        label = ctk.CTkLabel(frame, text=texto)
        label.pack(side="left", padx=10)

        valor = ctk.CTkLabel(frame, text="---")
        valor.pack(side="right", padx=10)

        return {"label": label, "valor": valor}

    # calcular: Obtiene los datos ingresados, calcula las métricas del modelo seleccionado (MM1 o MMc), y muestra los resultados y la gráfica.
    def calcular(self):
        self.boton_calcular.configure(state="disabled", text="Calculando...")

        try:
            if self.modelo_var.get() == "" or self.unidad_tiempo_var.get() == "":
                self.mostrar_error("Por favor selecciona un modelo y una unidad de tiempo.")
                return
            
            lambd = float(self.lambda_entry.get())
            mu = float(self.mu_entry.get())
            n_max = int(self.n_entry.get())
            
            if self.modelo_var.get() == "MMc":
                s = int(self.s_entry.get())
                resultado = mmc_metrics(lambd, mu, s, n_max)
            else:
                resultado = mm1_metrics(lambd, mu, n_max)

            if isinstance(resultado, str):
                self.mostrar_error(resultado)
                return

            self.mostrar_resultados(resultado)
            self.mostrar_grafica(resultado["Pn"])

            self.limpiar_campos_izq()

        except ValueError:
            self.mostrar_error("Error: Por favor, ingrese valores numéricos válidos.")
        
        finally:
            self.boton_calcular.configure(state="normal", text="¿Listo para calcular?")

    # mostrar_resultados: Se encarga de mostrar los resultados calculados (métricas y probabilidades) después de presionar el botón "Calcular".
    def mostrar_resultados(self, resultado):
        metricas = {
            "rho": resultado["rho (factor de uso)"],
            "Ls": resultado["Ls (clientes esperados en el sistema)"],
            "Lq": resultado["Lq (clientes esperados en la cola)"],
            "Ws": resultado["Ws (tiempo esperado en el sistema)"],
            "Wq": resultado["Wq (tiempo esperado en la cola)"],
            "P0": resultado["P0 (probabilidad del sistema vacío)"]
        }
        
        for key, value in metricas.items():
            self.labels_resultados[key]["valor"].configure(text=f"{value:.4f}")

        self.prob_text.configure(state="normal")
        self.prob_text.delete("1.0", "end")
        prob_texto = ""
        for i, p in enumerate(resultado["Pn"]):
            porcentaje = p * 100
            prob_texto += f"P{i} = {porcentaje:.2f}%\n"
        self.prob_text.insert("1.0", prob_texto)
        self.prob_text.configure(state="disabled")

    # limpiar_campos: Limpia los campos del panel izquierdo.
    def limpiar_campos_izq(self):
        self.lambda_entry.delete(0, "end")
        self.mu_entry.delete(0, "end")
        self.n_entry.delete(0, "end")
        self.s_entry.delete(0, "end")

        self.modelo_var.set("")
        self.unidad_tiempo_var.set("")
    
    # limpiar_campos_der: Limpia los campos del panel derecho.
    def limpiar_campos_der(self):
        for item in self.labels_resultados.values():
            item["valor"].configure(text="---")

        self.prob_text.configure(state="normal")
        self.prob_text.delete("1.0", "end")
        self.prob_text.configure(state="disabled")

        for widget in self.frame_grafica.winfo_children():
            widget.destroy()

    # mostrar_error: Crear una ventana popup para mostrar posibles errores.
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)
        self.limpiar_campos_izq()
        self.limpiar_campos_der()

    # mostrar_grafica: Grafica las probabilidades n-ésimas.
    def mostrar_grafica(self, Pn):
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6, 3), facecolor='white')
        ax = fig.add_subplot(111)

        barras = ax.bar(range(len(Pn)), Pn, color='#4A90E2', edgecolor='black', linewidth=0.5)

        ax.set_xlabel('n (número de clientes)', fontsize=12, color='black', labelpad=10)
        ax.set_ylabel('Pₙ (probabilidad)', fontsize=12, color='black', labelpad=10)
        ax.set_title('Distribución de Probabilidades Pₙ', fontsize=14, color='black', pad=15)

        fig.tight_layout()

        ax.set_facecolor('white')
        ax.grid(True, axis='y', linestyle='--', alpha=0.4)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.tick_params(colors='black', labelsize=10)

        for i, bar in enumerate(barras):
            altura = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, altura + 0.005, f"{altura:.2f}",
                    ha='center', va='bottom', fontsize=9, color='black')

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# ====================================================================================================
# FUNCION MAIN PARA VISTA EN INTERFAZ
# ====================================================================================================
if __name__ == "__main__":
    app = SimuladorColas()
    app.mainloop() 
