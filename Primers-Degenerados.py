import pandas as pd
import tkinter as tk
from tkinter import ttk, scrolledtext
from io import StringIO

def procesar_input():
    # Obtener el texto de la entrada
    input_text = entrada_texto.get("1.0", "end-1c")

    # Crear DataFrame a partir del input
    df = pd.read_csv(StringIO(input_text), sep='\s+', header=None, names=['ID', 'Sequence', 'Length'])

    # Aislar la columna 'Sequence'
    sequences = df['Sequence'].tolist()

    # Dividir cada secuencia en letras individuales
    letter_lists = [list(sequence) for sequence in sequences]

    # Crear un nuevo DataFrame
    letters_df = pd.DataFrame(letter_lists)

    # Función para obtener letras únicas y manejar el caso de "-"
    def obtener_letras(columna):
        if columna.value_counts().get("-", 0) >= len(columna) / 2:
            return "-"
        else:
            return set(columna.unique()) - set(["-"])

    # Aplicar la función a cada columna de letters_df
    resultado_por_columna = letters_df.apply(obtener_letras)

    # DataFrame con los resultados únicos
    resultados_df = pd.DataFrame(resultado_por_columna).transpose()

    # Función para convertir conjuntos a cadenas de texto y quitar corchetes
    def quitar_corchetes(letra):
        return str(letra).replace("{", "").replace("}", "").replace("'", "")

    # Aplicar la función a cada elemento del DataFrame
    resultados_df = resultados_df.applymap(quitar_corchetes)

    # Función para traducir los resultados de cada columna
    def traducir_resultados_columna(columna):
        # Obtener el resultado único de la columna
        resultado_unico = set(columna)

        # Traducir según las condiciones especificadas
        if "G, A" in resultado_unico or "A, G" in resultado_unico:
            return "R"
        elif "T, C" in resultado_unico or "C, T" in resultado_unico:
            return "Y"
        elif "A, C" in resultado_unico or "C, A" in resultado_unico:
            return "M"
        elif "G, T" in resultado_unico or "T, G" in resultado_unico:
            return "K"
        elif "G, C" in resultado_unico or "C, G" in resultado_unico:
            return "S"
        elif "A, T" in resultado_unico or "T, A" in resultado_unico:
            return "W"
        elif "A, C, T" in resultado_unico or "A, T, C" in resultado_unico or "T, C, A" in resultado_unico \
                or "T, A, C" in resultado_unico or "C, A, T" in resultado_unico or "C, T, A" in resultado_unico:
            return "H"
        elif "G, T, C" in resultado_unico or "G, C, T" in resultado_unico or "T, C, G" in resultado_unico \
                or "T, G, C" in resultado_unico or "C, G, T" in resultado_unico or "C, T, G" in resultado_unico:
            return "B"
        elif "G, A, C" in resultado_unico or "G, C, A" in resultado_unico or "A, C, G" in resultado_unico \
                or "A, G, C" in resultado_unico or "C, G, A" in resultado_unico or "C, A, G" in resultado_unico:
            return "V"
        elif "G, T, A" in resultado_unico or "G, A, T" in resultado_unico or "T, A, G" in resultado_unico \
                or "T, G, A" in resultado_unico or "A, G, T" in resultado_unico or "A, T, G" in resultado_unico:
            return "D"
        elif "G, A, T, C" in resultado_unico or "A, T, G, C" in resultado_unico or "T, C, A, G" in resultado_unico \
                or "G, A, C, T" in resultado_unico or "A, T, C, G" in resultado_unico or "T, G, C, A" in resultado_unico \
                or "G, T, A, C" in resultado_unico or "A, C, G, T" in resultado_unico or "C, G, A, T" in resultado_unico \
                or "G, T, C, A" in resultado_unico or "A, C, T, G" in resultado_unico or "C, G, T, A" in resultado_unico \
                or "G, C, A, T" in resultado_unico or "T, G, A, C" in resultado_unico or "C, A, T, G" in resultado_unico \
                or "G, C, T, A" in resultado_unico or "T, A, C, G" in resultado_unico or "C, T, A, G" in resultado_unico \
                or "A, G, T, C" in resultado_unico or "T, A, G, C" in resultado_unico or "C, T, G, A" in resultado_unico \
                or "A, G, C, T" in resultado_unico or "T, A, C, G" in resultado_unico or "T, G, C, A" in resultado_unico:
            return "N"
        else:
            return columna.iloc[0]

    # Aplicar la función a cada columna de resultados_df
    resultados_traducidos_columna = resultados_df.apply(traducir_resultados_columna)

    # Convertir resultados a una cadena de texto
    resultados_cadena = resultados_traducidos_columna.str.cat(sep='')

    # Mostrar los resultados en la caja de texto
    caja_resultados.delete(1.0, tk.END)  # Limpiar contenido anterior
    caja_resultados.insert(tk.END, resultados_cadena)

def limpiar_cajas():
    entrada_texto.delete(1.0, tk.END)
    caja_resultados.delete(1.0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Traductor de Secuencias")

# Ajustar tamaño de la ventana
ventana.geometry("800x600")

# Crear caja de texto para el input
entrada_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=60, height=20)
entrada_texto.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Crear botón para procesar el input
boton_procesar = ttk.Button(ventana, text="Procesar Input", command=procesar_input)
boton_procesar.grid(row=1, column=0, pady=5, sticky="w")

# Crear botón para limpiar cajas de texto
boton_limpiar = ttk.Button(ventana, text="Limpiar", command=limpiar_cajas)
boton_limpiar.grid(row=1, column=0, pady=5, padx=100, sticky="e")

# Crear caja de texto para mostrar los resultados
caja_resultados = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=60, height=20)
caja_resultados.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Texto de instrucciones
instrucciones_texto = """
Instrucciones de Uso:

1. Ingrese las secuencias en el formato especificado (60 pb por línea).
2. Haga clic en el botón 'Procesar Input' para traducir las secuencias.
3. Los resultados se mostrarán en la caja de texto inferior.
4. Utilice el botón 'Limpiar' para borrar las cajas de texto y comenzar de nuevo.

Créditos GitHub: fjosesala
"""

# Crear etiqueta para las instrucciones
etiqueta_instrucciones = ttk.Label(ventana, text=instrucciones_texto, wraplength=500, justify=tk.LEFT)
etiqueta_instrucciones.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configurar el peso de las columnas y filas para el correcto ajuste de la interfaz
ventana.columnconfigure(1, weight=1)
ventana.rowconfigure(0, weight=1)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
