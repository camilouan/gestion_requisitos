import tkinter as tk
from tkinter import messagebox
import sqlite3

# Clase para manejo de la base de datos
class BandaDB:
    def __init__(self):
        self.conn = sqlite3.connect('banda.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Banda (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT,
                                seguidores INTEGER)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Integrante (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT,
                                instrumento TEXT,
                                imagen TEXT,
                                seguidores INTEGER,
                                conciertos INTEGER,
                                ganancias REAL,
                                banda_id INTEGER,
                                FOREIGN KEY (banda_id) REFERENCES Banda(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Concierto (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fecha TEXT,
                                ganancias REAL)''')
        self.conn.commit()

    def agregar_banda(self, nombre, seguidores):
        self.cursor.execute("INSERT INTO Banda (nombre, seguidores) VALUES (?, ?)", (nombre, seguidores))
        self.conn.commit()

    def agregar_integrante(self, nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id):
        self.cursor.execute("INSERT INTO Integrante (nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                            (nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id))
        self.conn.commit()

    def agregar_concierto(self, fecha, ganancias):
        self.cursor.execute("INSERT INTO Concierto (fecha, ganancias) VALUES (?, ?)", (fecha, ganancias))
        self.conn.commit()

    def obtener_bandas_integrantes(self):
        bandas = []
        self.cursor.execute("SELECT * FROM Banda")
        for banda in self.cursor.fetchall():
            banda_info = {"banda": banda}
            self.cursor.execute("SELECT * FROM Integrante WHERE banda_id=?", (banda[0],))
            integrantes = self.cursor.fetchall()
            banda_info["integrantes"] = integrantes
            bandas.append(banda_info)
        return bandas

    def resetear_base_datos(self):
        self.cursor.execute("DELETE FROM Integrante")
        self.cursor.execute("DELETE FROM Banda")
        self.cursor.execute("DELETE FROM Concierto")
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()


# Clase principal de la aplicación
class AppBanda:
    def __init__(self, root):
        self.db = BandaDB()
        self.root = root
        self.root.title("🎶 Gestión de Bandas")
        self.root.geometry("700x600")
        self.color_fondo = "#e6f2ff"  # azul claro
        self.root.configure(bg=self.color_fondo)
        self.menu_principal()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def menu_principal(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="📌 Menú Principal", font=("Arial", 18, "bold"), bg=self.color_fondo).pack(pady=20)

        opciones = [
            ("🎵 Agregar Banda", self.form_banda),
            ("👤 Agregar Integrante", self.form_integrante),
            ("🎤 Agregar Concierto", self.form_concierto),
            ("📋 Ver Bandas e Integrantes", self.ver_bandas_integrantes),
            ("📅 Ver Conciertos", self.ver_conciertos),
            ("🧹 Resetear Base de Datos", self.resetear_datos),
            ("❌ Salir", self.salir_app)
        ]

        for texto, accion in opciones:
            tk.Button(self.root, text=texto, width=35, height=2, font=("Arial", 11), bg="white", command=accion).pack(pady=5)

    def form_banda(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="🎵 Agregar Banda", font=("Arial", 16, "bold"), bg=self.color_fondo).pack(pady=15)

        nombre_var = tk.StringVar()
        seguidores_var = tk.StringVar()

        for label, var in [("Nombre:", nombre_var), ("Seguidores:", seguidores_var)]:
            tk.Label(self.root, text=label, bg=self.color_fondo).pack()
            tk.Entry(self.root, textvariable=var, width=40).pack()

        def guardar():
            try:
                self.db.agregar_banda(nombre_var.get(), int(seguidores_var.get()))
                messagebox.showinfo("✅ Éxito", "Banda registrada.")
                self.menu_principal()
            except:
                messagebox.showerror("❌ Error", "Verifica los datos.")

        tk.Button(self.root, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(self.root, text="⬅ Volver", command=self.menu_principal).pack()

    def form_integrante(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="👤 Agregar Integrante", font=("Arial", 16, "bold"), bg=self.color_fondo).pack(pady=15)

        campos = ["Nombre", "Instrumento", "Imagen", "Seguidores", "Conciertos", "Ganancias", "ID Banda"]
        entradas = {}

        for campo in campos:
            tk.Label(self.root, text=campo + ":", bg=self.color_fondo).pack()
            entradas[campo] = tk.Entry(self.root, width=40)
            entradas[campo].pack()

        def guardar():
            try:
                self.db.agregar_integrante(
                    entradas["Nombre"].get(),
                    entradas["Instrumento"].get(),
                    entradas["Imagen"].get(),
                    int(entradas["Seguidores"].get()),
                    int(entradas["Conciertos"].get()),
                    float(entradas["Ganancias"].get()),
                    int(entradas["ID Banda"].get())
                )
                messagebox.showinfo("✅ Éxito", "Integrante agregado.")
                self.menu_principal()
            except:
                messagebox.showerror("❌ Error", "Datos inválidos.")

        tk.Button(self.root, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(self.root, text="⬅ Volver", command=self.menu_principal).pack()

    def form_concierto(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="🎤 Agregar Concierto", font=("Arial", 16, "bold"), bg=self.color_fondo).pack(pady=15)

        fecha_var = tk.StringVar()
        ganancias_var = tk.StringVar()

        for label, var in [("Fecha (YYYY-MM-DD):", fecha_var), ("Ganancias:", ganancias_var)]:
            tk.Label(self.root, text=label, bg=self.color_fondo).pack()
            tk.Entry(self.root, textvariable=var, width=40).pack()

        def guardar():
            try:
                self.db.agregar_concierto(fecha_var.get(), float(ganancias_var.get()))
                messagebox.showinfo("✅ Éxito", "Concierto registrado.")
                self.menu_principal()
            except:
                messagebox.showerror("❌ Error", "Datos inválidos.")

        tk.Button(self.root, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(self.root, text="⬅ Volver", command=self.menu_principal).pack()

    def ver_bandas_integrantes(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="🎸 Bandas e Integrantes", font=("Arial", 16, "bold"), bg=self.color_fondo).pack(pady=15)

        try:
            data = self.db.obtener_bandas_integrantes()
            for item in data:
                banda = item["banda"]
                tk.Label(self.root, text=f"🎵 {banda[1]} (Seguidores: {banda[2]})", font=("Arial", 12, "bold"), bg=self.color_fondo).pack()
                for integrante in item["integrantes"]:
                    info = f"    👤 {integrante[1]} - {integrante[2]} (🎯 {integrante[4]} seguidores)"
                    tk.Label(self.root, text=info, bg=self.color_fondo).pack(anchor="w", padx=20)
        except:
            messagebox.showerror("❌ Error", "No se pudo cargar la información.")

        tk.Button(self.root, text="⬅ Volver", command=self.menu_principal).pack(pady=10)

    def ver_conciertos(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="📅 Conciertos Registrados", font=("Arial", 16, "bold"), bg=self.color_fondo).pack(pady=15)

        self.db.cursor.execute("SELECT * FROM Concierto")
        conciertos = self.db.cursor.fetchall()

        for c in conciertos:
            texto = f"🎫 {c[1]} - Ganancias: ${c[2]}"
            tk.Label(self.root, text=texto, bg=self.color_fondo).pack(anchor="w", padx=20)

        tk.Button(self.root, text="⬅ Volver", command=self.menu_principal).pack(pady=10)

    def resetear_datos(self):
        confirmacion = messagebox.askyesno("⚠ Confirmar", "¿Estás seguro de eliminar todos los datos?")
        if confirmacion:
            self.db.resetear_base_datos()
            messagebox.showinfo("🧹 Base de Datos", "Todos los datos fueron eliminados.")

    def salir_app(self):
        self.db.cerrar_conexion()
        self.root.destroy()


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AppBanda(root)
    root.mainloop()

