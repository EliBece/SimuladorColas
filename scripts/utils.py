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

# =================================================================================
# TEORIA DE COLAS [MODELO MM1 - MMc]
# =================================================================================
# Este programa tiene como objetivo realizar lo siguiente:
#   - Indicar al usuario que modelo desea trabajar.
#   - Pedirle al usuario los parámetros de entrada necesarios.
#   - Validar los parámetros de entrada para evitar condiciones críticas.
#   - Obtener las métricas para cada sistema.
#   - Obtener probabilidades n-ésimas para cada sistema.

from math import factorial
import matplotlib.pyplot as plt



# ====================================================================================================
# MODELO MM1 METRICAS
# ====================================================================================================
def mm1_metrics(lambd, mu, n_max):
    if lambd >= mu:
        return "\nERROR: El sistema colapsa (λ ≥ μ)."

    rho = lambd / mu
    Ls = rho / (1 - rho)
    Lq = Ls - rho
    Ws = 1 / (mu - lambd)
    Wq = rho / (mu - lambd)
    P0 = 1 - rho
    Pn = [(1 - rho) * rho**n for n in range(n_max + 1)]

    return {
        "rho (factor de uso)": rho, 
        "Ls (clientes esperados en el sistema)": Ls, 
        "Lq (clientes esperados en la cola)": Lq, 
        "Ws (tiempo esperado en el sistema)": Ws, 
        "Wq (tiempo esperado en la cola)": Wq, 
        "P0 (probabilidad del sistema vacío)": P0, 
        "Pn": Pn
    }

# ====================================================================================================
# MODELO MMc METRICAS
# ====================================================================================================
def mmc_metrics(lambd, mu, s, n_max):
    rho = lambd / (s * mu)

    if rho >= 1:
        return "\nERROR: El sistema colapsa (ρ ≥ 1)."

    sum_terms = sum((lambd / mu)**n / factorial(n) for n in range(s))
    last_term = ((lambd / mu)**s / (factorial(s) * (1 - rho)))
    P0 = 1 / (sum_terms + last_term)

    Lq = (P0 * ((lambd / mu)*s) * rho) / (factorial(s) * (1 - rho)*2)
    Ls = Lq + lambd / mu
    Wq = Lq / lambd
    Ws = Wq + 1 / mu
    c_bar = lambd / mu
    Pn = [((lambd / mu)**n / factorial(n)) * P0 if n < s else ((lambd / mu)**n / (factorial(s) * s**(n - s))) * P0 for n in range(n_max + 1)]

    return {
        "rho (factor de uso)": rho, 
        "Ls (clientes esperados en el sistema)": Ls, 
        "Lq (clientes esperados en la cola)": Lq, 
        "Ws (tiempo esperado en el sistema)": Ws, 
        "Wq (tiempo esperado en la cola)": Wq, 
        "c_bar (servidores ocupados)": c_bar,
        "P0 (probabilidad del sistema vacío)": P0, 
        "Pn": Pn
    }

# ====================================================================================================
# GRAFICAR PROBABILIDADES N
# ====================================================================================================
def plot_probabilities(Pn):
    plt.bar(range(len(Pn)), Pn, color='skyblue')
    plt.xlabel('n (número de clientes en el sistema)')
    plt.ylabel('Pₙ (probabilidad)')
    plt.title('Distribución de Probabilidades Pₙ')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.show()



# ====================================================================================================
# FUNCION MAIN PARA VISTA EN CONSOLA
# ====================================================================================================
# def main():
#     print("\n\n")
#     print("------------------------------------------------------------")
#     print("               Teoría de Colas: MM1 o MMc                   ")
#     print("------------------------------------------------------------")
#     print(">> Bienvenido a la Teoría de Colas...\n\n")
#     print("  - Para seleccionar un modelo tipo MM1 escriba 'MM1'.")
#     print("  - Para seleccionar un modelo tipo MMc escriba 'MMc'.")
#     print("  - Debe colocar los valores por hora o minutos según corresponda.")
#     print("  - Requerimos saber el valor de λ, μ y el número de probabilidades a calcular.\n\n")

#     print("------------INGRESA LOS DATOS NECESARIOS------------")
#     try:
#         unidad_tiempo = input("   >> ¿Deseas trabajar en HORAS o MINUTOS (escribe)?: ").strip().lower()
#         if unidad_tiempo not in ["horas", "minutos"]:
#             print("\nERROR: Unidad no válida. Usa 'horas' o 'minutos'.")
#             return

#         model = input("   >> Selecciona el modelo (MM1 o MMc): ").strip().upper()
#         lambd = float(input(f"   >> Ingrese la Tasa de Llegada λ (clientes/{unidad_tiempo}): "))
#         mu = float(input(f"   >> Ingrese la Tasa de Servicio μ (clientes/{unidad_tiempo}): "))
#         n_max = int(input("   >> ¿Cuántas probabilidades P_n deseas calcular (probabilidades n-ésimas)?: "))
        
#         if model == "MMc":
#             s = int(input("   >> Ingrese el número de servidores s: "))
#         else:
#             s = None
#     except ValueError:
#         print("\nERROR: Algún dato no fue del tipo esperado...")
#         return

#     if model == "MM1":
#         result = mm1_metrics(lambd, mu, n_max)
#     elif model == "MMc":
#         result = mmc_metrics(lambd, mu, s, n_max)
#     else:
#         print("\nERROR: Modelo no reconocido. Usa MM1 o MMc.")
#         return

#     if isinstance(result, str):
#         print(result)
#         return

#     print("\n\n------------RESULTADOS OBTENIDOS------------")
#     print(f"   Modelo Seleccionado: {model}")
#     print(f"   Unidad de tiempo: {unidad_tiempo.capitalize()}\n")

#     print("   Parámetros Clave:")
#     for k, v in result.items():
#         if k != "Pn":
#             if "tiempo" in k:
#                 unidad = unidad_tiempo
#             elif "clientes" in k:
#                 unidad = "clientes"
#             elif "servidores" in k:
#                 unidad = "servidores"
#             elif "factor" in k:
#                 unidad = "(sin unidad)"
#             elif "probabilidad" in k:
#                 unidad = "(0 a 1)"
#             else:
#                 unidad = ""

#             print(f"     * {k:<45} = {v:>8.4f} {unidad}")

#     print("\n   Probabilidades Pₙ (hasta n = {}):".format(n_max))
#     for i, p in enumerate(result["Pn"]):
#         print(f"    * P{i} = {p:.4f}")

#     print("   \nImprimiendo gráficas:")
#     plot_probabilities(result["Pn"])

# if __name__ == "_main_":
#     main()
