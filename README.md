# Simulador de Colas Markoviano - [M/M/1 - M/M/s]

## 🚨 Licencia
Este proyecto está licenciado bajo la Licencia MIT.  
Consulta el archivo [LICENSE](./LICENSE) para más información.

## 🌱 Descripción del Proyecto

**Nombre del Proyecto: Simulador de Teoría de Colas Markoviano**

👉 **¿Solo quieres probar el programa sin leer todo?:** Dirígete al final de esta lectura.

Este proyecto fue desarrollado como parte del curso de **Simulación** y tiene como objetivo implementar, analizar y visualizar el comportamiento de sistemas de colas bajo los modelos **M/M/1** y **M/M/s**. El programa permite calcular métricas clave como el número promedio de clientes en el sistema (Ls), en la cola (Lq), el tiempo promedio en el sistema (Ws), el tiempo en la cola (Wq), la probabilidad de que el sistema esté vacío (P₀), entre otras.

<div style="text-align:center;">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXk0ZnlzbTlsenBkYjQ2NzV3NmQ1cWhyNzAzdTgzczl1dndqdmp3NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/citBl9yPwnUOs/giphy.gif">
</div>

## ✅ Características principales
- Soporta análisis para **M/M/1** (una sola cola, un servidor) y **M/M/s** (una sola cola, varios servidores).
- Interfaz gráfica de consola para introducir parámetros fácilmente.
- Validación de datos de entrada para evitar errores en la simulación.
- Resultados claros y bien organizados.
- Generación de gráficas automáticas para una mejor visualización.
- Código modular y comentado.

## 📁 Estructura del Proyecto
La estructura del proyecto se muestra a continuación: 
```bash
📦 ProyectoFinal_SIM800_App/
├── images/
│   └── funny_image.png          # Imagen decorativa
├── scripts/
│   ├── interface.py             # Menú e interacción con el usuario
│   └── utils.py                 # Lógica de cálculo y funciones auxiliares
├── README.md                    # Este archivo
└── requirements.txt             # Dependencias necesarias
```
## 📦 Scripts Python
- `interface.py`: Archivo principal que se ejecuta. Sirve como interfaz del usuario (valida datos, solicita datos, llama a las funciones matemáticas y muestra resultados.)
- `utils.py`: Contiene las funciones principales de cálculo para las métricas de ambos modelos.

## 🧰 Importante Dependencias
El archivo `requirements.txt` sirve para instalar librerías de Python necesarias en el proyecto, como: 
```bash
Pillow              # Para cargar y manipular imágenes
customtkinter       # Versión mejorada y estilizada de tkinter (interfaces gráficas de usuario)
matplotlib          # Para generar gráficas
```

## 🚀 Archivo EXE
Puede descargar el ejecutable final `SimuladorMarkoviano.exe` en este enlace para probar el programa final:
- [Drive con Ejecutable Final "SimuladorMarkoviano.exe"](https://drive.google.com/drive/folders/191dNO9RdC-S_U2i7LdTagC2iudagq62d?usp=sharing)

**⚠️ IMPORTANTE:** Este archivo está compilado solo para Windows. Si el navegador o antivirus muestra una advertencia, es por tratarse de un archivo `.exe`. Puede confiar en él, fue generado a partir de este mismo proyecto. Si se encuentra en otro sistema operativo, puede correr el proyecto desde el código fuente usando Python (asegúrese de tener las dependencias instaladas `requirements.txt`).
