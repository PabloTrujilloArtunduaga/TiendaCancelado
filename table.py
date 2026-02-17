import tkinter as tk
from tkinter import ttk

def crear_tabla(parent, columnas, datos):
    card = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )
    card.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    container = tk.Frame(card, bg="white")
    container.pack(fill="both", expand=True, padx=15, pady=15)

    style = ttk.Style()
    style.configure("Treeview",
        background="white",
        foreground="#111827",
        rowheight=30,
        fieldbackground="white",
        font=("Segoe UI", 10)
    )

    style.configure("Treeview.Heading",
        background="#1f2937",
        foreground="white",
        font=("Segoe UI", 11, "bold")
    )

    style.map("Treeview",
        background=[("selected", "#2563eb")],
        foreground=[("selected", "white")]
    )

    tree = ttk.Treeview(container, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.tag_configure("odd", background="#f8fafc")
    tree.tag_configure("even", background="#ffffff")

    for i, fila in enumerate(datos):
        tree.insert("", "end", values=fila,
                    tags=("even" if i % 2 == 0 else "odd",))

    scroll_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    return tree
