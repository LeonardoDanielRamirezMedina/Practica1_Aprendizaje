import tkinter as tk
from tkinter import scrolledtext

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
        formula = f"A ∧ B" if operador == 'and' else "A V B"
        etiqueta_resultado.config(text=f"Operador identificado: {operador.upper()}\n"
                                       f"Proposiciones simples:\n"
                                       f"A: {proposiciones_simples[0]}\n"
                                       f"B: {proposiciones_simples[1]}\n"
                                       f"Fórmula: {formula}")
        boton_cerrar.pack()  # Mostrar el botón de cerrar
    else:
        etiqueta_resultado.config(text="Proposición no válida")

def cerrar_y_mostrar():
    ventana.destroy()  # Cerrar la ventana principal
    mostrar_tabla_verdad(operador)
    mostrar_arbol(operador)

# Función para mostrar la tabla de verdad en una ventana
def mostrar_tabla_verdad(operador):
    # Crear la ventana principal
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Tabla de verdad para {operador.upper()}")
    
    # Crear un widget de texto con desplazamiento
    texto = scrolledtext.ScrolledText(ventana_tabla, width=30, height=10)
    texto.pack()
    
    # Agregar la tabla de verdad al widget de texto
    texto.insert(tk.END, f"Tabla de verdad para {operador.upper()}:\n\n")
    texto.insert(tk.END, "A | B | Resultado\n")
    texto.insert(tk.END, "--|---|----------\n")
    
    for A in [1, 0]:
        for B in [1, 0]:
            if operador == 'and':
                resultado = A and B
            elif operador == 'or':
                resultado = A or B
            texto.insert(tk.END, f"{A} | {B} | {resultado}\n")
    
    ventana_tabla.mainloop()

# Función para mostrar el diagrama de árbol
def mostrar_arbol(operador):
    # Crear la ventana principal
    ventana_arbol = tk.Tk()
    ventana_arbol.title(f"Diagrama de árbol para {operador.upper()}")
    
    # Crear un canvas para dibujar el árbol
    canvas = tk.Canvas(ventana_arbol, width=600, height=400, bg="white")
    canvas.pack()
    
    # Coordenadas iniciales
    x0, y0 = 300, 50
    dx, dy = 100, 100
    
    # Mostrar proposiciones simples en la parte superior
    canvas.create_text(x0, y0 - 40, text=f"A: {proposiciones_simples[0]}", font=("Arial", 12, "bold"))
    canvas.create_text(x0, y0 - 20, text=f"B: {proposiciones_simples[1]}", font=("Arial", 12, "bold"))
    
    # Dibujar el nodo raíz
    nodo_raiz = f"A {operador.upper()} B"
    canvas.create_text(x0, y0, text=nodo_raiz, font=("Arial", 12, "bold"))
    
    # Dibujar los nodos y aristas basados en la tabla de verdad
    for i, A in enumerate([0, 1]):
        x1, y1 = x0 - dx + i * 2 * dx, y0 + dy
        nodo_A = f"A={A}"
        canvas.create_text(x1, y1, text=nodo_A, font=("Arial", 12))
        canvas.create_line(x0, y0, x1, y1)
        
        for j, B in enumerate([0, 1]):
            x2, y2 = x1 - dx/2 + j * dx, y1 + dy
            nodo_B = f"B={B}"
            canvas.create_text(x2, y2, text=nodo_B, font=("Arial", 12))
            canvas.create_line(x1, y1, x2, y2)
            
            if operador == 'and':
                resultado = A and B
            elif operador == 'or':
                resultado = A or B
            nodo_resultado = f"R={resultado}"
            canvas.create_text(x2, y2 + dy, text=nodo_resultado, font=("Arial", 12))
            canvas.create_line(x2, y2, x2, y2 + dy)
    
    # Ejecutar el bucle principal de la ventana
    ventana_arbol.mainloop()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Proposiciones")

# Crear y colocar los widgets
tk.Label(ventana, text="Ingresa la proposición:").pack()
entrada_proposicion = tk.Entry(ventana, width=50)
entrada_proposicion.pack()

boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_proposicion)
boton_procesar.pack()

etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()

# Botón para cerrar la ventana y mostrar la tabla y el diagrama
boton_cerrar = tk.Button(ventana, text="Cerrar y mostrar resultados", command=cerrar_y_mostrar)
boton_cerrar.pack_forget()  # Ocultar el botón inicialmente

# Iniciar el bucle principal de la interfaz
ventana.mainloop()