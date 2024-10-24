import tkinter as tk
from tkinter import scrolledtext
from itertools import product

def identificar_operador(proposicion):
    if ' y ' in proposicion:
        operador = 'and'
        proposiciones_simples = proposicion.split(' y ')
    elif ' o ' in proposicion:
        operador = 'or'
        proposiciones_simples = proposicion.split(' o ')
    else:
        return None
    return operador, [p.strip() for p in proposiciones_simples]

def procesar_proposicion():
    proposicion = entrada_proposicion.get().lower()
    resultado = identificar_operador(proposicion)
    
    if isinstance(resultado, tuple):
        global operador, proposiciones_simples
        operador, proposiciones_simples = resultado
        formula = ' ∧ '.join(['A', 'B', 'C', 'D', 'E'][:len(proposiciones_simples)]) if operador == 'and' else ' ∨ '.join(['A', 'B', 'C', 'D', 'E'][:len(proposiciones_simples)])
        text_result = f"Operador identificado: {operador.upper()}\nProposiciones simples:\n"
        for i, prop in enumerate(proposiciones_simples):
            text_result += f"{chr(65 + i)}: {prop}\n"
        text_result += f"Fórmula: {formula}"
        etiqueta_resultado.config(text=text_result)
        boton_cerrar.pack()  # Mostrar el botón de cerrar
    else:
        etiqueta_resultado.config(text="Proposición no válida")

def cerrar_y_mostrar():
    ventana.destroy()  # Cerrar la ventana principal
    mostrar_tabla_verdad(operador, proposiciones_simples)
    mostrar_arbol(operador)

# Función para mostrar la tabla de verdad en una ventana
def mostrar_tabla_verdad(operador, proposiciones_simples):
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Tabla de verdad para {operador.upper()}")
    texto = scrolledtext.ScrolledText(ventana_tabla, width=50, height=15)
    texto.pack()
    
    texto.insert(tk.END, f"Tabla de verdad para {operador.upper()}:\n\n")
    headers = ' | '.join([chr(65 + i) for i in range(len(proposiciones_simples))]) + " | Resultado\n"
    texto.insert(tk.END, headers)
    texto.insert(tk.END, "--|" * (len(proposiciones_simples) + 1) + "----------\n")
    
    def evaluar_resultado(values, operador):
        if operador == 'and':
            return int(all(values))
        elif operador == 'or':
            return int(any(values))

    for valores in product([1, 0], repeat=len(proposiciones_simples)):
        resultado = evaluar_resultado(valores, operador)
        valores_str = ' | '.join(map(str, valores)) + f" | {resultado}\n"
        texto.insert(tk.END, valores_str)
    
    ventana_tabla.mainloop()

# Función para mostrar el diagrama de árbol con scroll
def mostrar_arbol(operador):
    ventana_arbol = tk.Tk()
    ventana_arbol.title(f"Diagrama de árbol para {operador.upper()}")

    frame = tk.Frame(ventana_arbol)
    frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(frame, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    draw_area = tk.Frame(canvas)
    canvas.create_window((0,0), window=draw_area, anchor="nw")

    x0, y0 = 800, 50  # Coordenada inicial centrada
    dx, dy = 100, 100  # Separación reducida entre nodos

    for i, prop in enumerate(proposiciones_simples):
        tk.Label(draw_area, text=f"{chr(65 + i)}: {prop}", font=("Arial", 12, "bold")).grid(row=0, column=i*dx)

    nodo_raiz = f" {operador.upper()} ".join([chr(65 + i) for i in range(len(proposiciones_simples))])
    tk.Label(draw_area, text=nodo_raiz, font=("Arial", 12, "bold")).grid(row=1, columnspan=dx*len(proposiciones_simples))

    def dibujar_nodos(draw_area, prev_x, prev_y, depth, current_vars):
        if depth == len(proposiciones_simples):
            return
        for val in [0, 1]:
            x = prev_x - (dx / 2) * (2 ** (len(proposiciones_simples) - depth - 1)) + val * (dx * (2 ** (len(proposiciones_simples) - depth - 1)))
            nodo = f"{chr(65 + depth)}={val}"
            tk.Label(draw_area, text=nodo, font=("Arial", 12)).grid(row=prev_y + dy, column=int(x))
            dibujar_nodos(draw_area, x, prev_y + dy, depth + 1, current_vars + [val])

    dibujar_nodos(draw_area, x0, y0, 0, [])

    ventana_arbol.mainloop()

ventana = tk.Tk()
ventana.title("Analizador de Proposiciones")
tk.Label(ventana, text="Ingresa la proposición:").pack()
entrada_proposicion = tk.Entry(ventana, width=70)
entrada_proposicion.pack()
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_proposicion)
boton_procesar.pack()
etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()
boton_cerrar = tk.Button(ventana, text="Cerrar y mostrar resultados", command=cerrar_y_mostrar)
boton_cerrar.pack_forget()

ventana.mainloop()
