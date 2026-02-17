import tkinter as tk
import tkinter.messagebox as messagebox

def abrir_usuario(nombre, windows):
    user_win = tk.Toplevel()
    user_win.title("Usuario")
    user_win.config(bg="lightyellow")
    user_win.geometry("400x300")
    user_win.state("zoomed")

    user_win.grid_rowconfigure(0, weight=1)
    user_win.grid_columnconfigure(1, weight=1)

    # ---------------------------------------
    # SIDEBAR
    # ---------------------------------------
    sidebar = tk.Frame(user_win, bg="#34495e", width=180)
    sidebar.grid(row=0, column=0, sticky="ns")

    tk.Label(
        sidebar,
        text="USUARIO",
        bg="#34495e",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    
    def cerrar_sesion():
        user_win.destroy()
        windows.deiconify()
        windows.state("zoomed")

    # ---------------------------------------
    # CONTENEDOR DE PÁGINAS
    # ---------------------------------------
    container = tk.Frame(user_win, bg="white")
    container.grid(row=0, column=1, sticky="nsew")

    pagina_inicio = tk.Frame(container, bg="white")
    pagina_productos = tk.Frame(container, bg="white")
    pagina_compras = tk.Frame(container, bg="white")

    for frame in (pagina_inicio, pagina_productos, pagina_compras):
        frame.grid(row=0, column=0, sticky="nsew")

    # ---------------------------------------
    # PÁGINA INICIO
    # ---------------------------------------
    tk.Label(
        pagina_inicio,
        text=f"Bienvenido, {nombre}",
        font=("Arial", 22),
        bg="white"
    ).pack(pady=40)

    tk.Label(
        pagina_inicio,
        text="Selecciona una opción del menú",
        font=("Arial", 14),
        bg="white",
        fg="gray"
    ).pack()

    # ---------------------------------------
    # PÁGINA PRODUCTOS
    # ---------------------------------------
    tk.Label(
        pagina_productos,
        text="Productos disponibles",
        font=("Arial", 22),
        bg="white"
    ).pack(pady=40)

    tk.Label(
        pagina_productos,
        text="Aquí el usuario puede ver productos (solo lectura)",
        font=("Arial", 13),
        bg="white",
        fg="gray"
    ).pack()

    # ---------------------------------------
    # PÁGINA COMPRAS
    # ---------------------------------------
    tk.Label(
        pagina_compras,
        text="Mis compras",
        font=("Arial", 22),
        bg="white"
    ).pack(pady=40)

    tk.Label(
        pagina_compras,
        text="Historial de compras del usuario",
        font=("Arial", 13),
        bg="white",
        fg="gray"
    ).pack()

    # ---------------------------------------
    # FUNCIÓN PARA MOSTRAR PÁGINAS
    # ---------------------------------------
    def mostrar(frame):
        frame.tkraise()

    # ---------------------------------------
    # BOTONES SIDEBAR
    # ---------------------------------------
    tk.Button(
        sidebar, text="Inicio", width=18,
        command=lambda: mostrar(pagina_inicio)
    ).pack(pady=8)

    tk.Button(
        sidebar, text="Productos", width=18,
        command=lambda: mostrar(pagina_productos)
    ).pack(pady=8)

    tk.Button(
        sidebar, text="Mis compras", width=18,
        command=lambda: mostrar(pagina_compras)
    ).pack(pady=8)

    # ---------------------------------------
    # CERRAR SESIÓN
    # ---------------------------------------
    tk.Button(
        sidebar,
        text="Cerrar Sesión",
        width=18,
        bg="#e74c3c",
        fg="white",
        command=cerrar_sesion
    ).pack(side="bottom", pady=20)

    mostrar(pagina_inicio)
