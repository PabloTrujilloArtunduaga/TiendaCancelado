import tkinter as tk
import tkinter.messagebox as messagebox
from db import conectar
import psycopg2
from crud_producto import crud_producto
from crud_user import crud_usuario
from table import crear_tabla


def abrir_admin(nombre, windows):
    admin_win = tk.Toplevel()
    admin_win.title("Administrador")
    admin_win.geometry("400x300")
    admin_win.state("zoomed")
    admin_win.config(bg="#ecf0f1")

    admin_win.grid_rowconfigure(0, weight=1)
    admin_win.grid_columnconfigure(1, weight=1)

    # ---------------------------------------
    # FUNCIÓN CERRAR SESIÓN
    # ---------------------------------------
    def cerrar_sesion():
        admin_win.destroy()
        windows.deiconify()
        windows.state("zoomed")

    # ---------------------------------------
    # SIDEBAR
    # ---------------------------------------
    sidebar = tk.Frame(admin_win, bg="#1f2a36", width=200)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)

    tk.Label(
        sidebar,
        text="ADMINISTRADOR",
        bg="#1f2a36",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=(30, 40))

    # ---------------------------------------
    # CONTENEDOR DE PÁGINAS
    # ---------------------------------------
    container = tk.Frame(admin_win, bg="#ecf0f1")
    container.grid(row=0, column=1, sticky="nsew")

    pagina_inicio = tk.Frame(container, bg="white")
    pagina_productos = tk.Frame(container, bg="white")
    pagina_usuarios = tk.Frame(container, bg="white")
    pagina_ventas = tk.Frame(container, bg="white")

    for frame in (pagina_inicio, pagina_productos, pagina_usuarios, pagina_ventas):
        frame.grid(row=0, column=0, sticky="nsew")

    # ---------------------------------------
    # PÁGINA INICIO
    # ---------------------------------------
  # ---------------------------------------
# PÁGINA INICIO
# ---------------------------------------
    tk.Label(
        pagina_inicio,
        text=f"Bienvenido, {nombre}",
        font=("Arial", 16),
        bg="white",
        fg="gray"
    ).pack(pady=(0, 30))

    # DESCRIPCIÓN GENERAL
    descripcion = (
        "Desde este panel puedes administrar completamente la tienda.\n\n"
        "Aquí podrás:\n"
        "• Gestionar productos (crear, editar y controlar stock)\n"
        "• Administrar usuarios y sus roles\n"
        "• Visualizar y gestionar las ventas\n\n"
        "Utiliza el menú lateral para navegar entre las secciones."
    )

    tk.Label(
        pagina_inicio,
        text=descripcion,
        font=("Arial", 13),
        bg="white",
        fg="#34495e",
        justify="left"
    ).pack(pady=20)

    # ---------------------------------------
    # TARJETAS INFORMATIVAS
    # ---------------------------------------
    cards_container = tk.Frame(pagina_inicio, bg="white")
    cards_container.pack(pady=40)

    def crear_card(parent, titulo, texto):
        card = tk.Frame(parent, bg="#ecf0f1", width=260, height=140)
        card.pack(side="left", padx=15)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=titulo,
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        tk.Label(
            card,
            text=texto,
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#555",
            wraplength=220,
            justify="center"
        ).pack(padx=10)

    # TARJETAS
    crear_card(
        cards_container,
        "📦 Productos",
        "Administra el catálogo de productos, precios, stock y proveedores."
    )

    crear_card(
        cards_container,
        "👤 Usuarios",
        "Gestiona usuarios registrados, roles y permisos del sistema."
    )

    crear_card(
        cards_container,
        "💰 Ventas",
        "Consulta y administra las ventas realizadas en la tienda."
    )


    # ---------------------------------------
    # PÁGINA PRODUCTOS
    # ---------------------------------------
    tk.Label(
        pagina_productos,
        text="Gestión de Productos",
        font=("Arial", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    frame_tabla = tk.Frame(pagina_productos, bg="white")
    frame_tabla.pack(fill="both", expand=True, padx=20)

    frame_formulario = tk.Frame(pagina_productos, bg="white")
    frame_formulario.pack(fill="x", padx=20, pady=10)

    columns_productos = (
        "ID", "Producto", "Descripcion", "Categoria",
        "Precio", "Stock", "Proveedor", "Creacion", "Activo"
    )

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_producto, nombre, descripcion, categoria,
                       precio, stock, proveedor, fecha_creacion, activo
                FROM productos
                ORDER BY id_producto ASC
            """)
            filas_productos = cur.fetchall()

    tabla_productos = crear_tabla(frame_tabla, columns_productos, filas_productos)

    def cargar_productos():
        tabla_productos.delete(*tabla_productos.get_children())
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_producto, nombre, descripcion, categoria,
                           precio, stock, proveedor, fecha_creacion, activo
                    FROM productos
                    ORDER BY id_producto ASC
                """)
                for fila in cur.fetchall():
                    tabla_productos.insert("", tk.END, values=fila)

    cargar_formulario = crud_producto(frame_formulario, cargar_productos)

    def al_seleccionar(event):
        seleccion = tabla_productos.focus()
        if seleccion:
            valores = tabla_productos.item(seleccion, "values")
            cargar_formulario(valores)

    tabla_productos.bind("<<TreeviewSelect>>", al_seleccionar)

    # ---------------------------------------
    # PÁGINA USUARIOS
    # ---------------------------------------
    tk.Label(
        pagina_usuarios,
        text="Gestión de Usuarios",
        font=("Arial", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    frame_tabla = tk.Frame(pagina_usuarios, bg="white")
    frame_tabla.pack(fill="both", expand=True, padx=20)

    frame_formulario = tk.Frame(pagina_usuarios, bg="white")
    frame_formulario.pack(fill="x", padx=20, pady=10)

    columns_usuarios = ("ID", "Nombre", "Rol ID", "Rol")

    
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT u.id, u.nombre, r.id AS rol_id, r.nombre
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                ORDER BY u.id
            """)
            filas_usuarios = cur.fetchall()

    tabla_user = crear_tabla(frame_tabla, columns_usuarios, filas_usuarios)

    def cargar_user():
        tabla_user.delete(*tabla_user.get_children())
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT u.id, u.nombre, r.id AS rol_id, r.nombre
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                ORDER BY u.id
            """)
                for fila in cur.fetchall():
                    tabla_user.insert("", tk.END, values=fila)
        

    cargar_formulario_user = crud_usuario(frame_formulario, cargar_user)
    
    def al_seleccionar_user(event):
        seleccion = tabla_user.focus()
        if seleccion:
            valores = tabla_user.item(seleccion, "values")
            cargar_formulario_user(valores)

    tabla_user.bind("<<TreeviewSelect>>", al_seleccionar_user)

    # ---------------------------------------
    # PÁGINA VENTAS
    # ---------------------------------------
    tk.Label(
        pagina_ventas,
        text="Gestión de Ventas",
        font=("Arial", 22, "bold"),
        bg="white"
    ).pack(pady=40)

    # ---------------------------------------
    # NAVEGACIÓN
    # ---------------------------------------
    def mostrar(frame):
        frame.tkraise()

    btn_style = {
        "width": 18,
        "height": 2,
        "bg": "#34495e",
        "fg": "white",
        "activebackground": "#5dade2",
        "bd": 0,
        "font": ("Arial", 11)
    }

    tk.Button(sidebar, text="Inicio",
              command=lambda: mostrar(pagina_inicio), **btn_style).pack(pady=6)

    tk.Button(sidebar, text="Productos",
              command=lambda: mostrar(pagina_productos), **btn_style).pack(pady=6)

    tk.Button(sidebar, text="Usuarios",
              command=lambda: mostrar(pagina_usuarios), **btn_style).pack(pady=6)

    tk.Button(sidebar, text="Ventas",
              command=lambda: mostrar(pagina_ventas), **btn_style).pack(pady=6)

    # ---------------------------------------
    # BOTÓN CERRAR SESIÓN
    # ---------------------------------------
    tk.Button(
        sidebar,
        text="Cerrar Sesión",
        width=18,
        height=2,
        bg="#c0392b",
        fg="white",
        bd=0,
        font=("Arial", 11, "bold"),
        activebackground="#e74c3c",
        command=cerrar_sesion
    ).pack(side="bottom", pady=25)

    mostrar(pagina_inicio)
