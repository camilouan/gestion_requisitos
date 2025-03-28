import pyodbc

class BandaDB:
    def __init__(self):
        """ Configuración de la conexión a SQL Server """
        self.server = 'DESKTOP-BF307G4\\SQLEXPRESS01'  # Nombre del servidor poner el nombre de tu servidor si es local el nombre del pc mas sqlexpress01
        self.database = 'BandaDB'  
        self.driver = '{ODBC Driver 17 for SQL Server}'  # Driver para SQL Server
        self.username = ''  # Usuario de SQL Server (si usas autenticación SQL)
        self.password = ''  # Contraseña (si usas autenticación SQL)

        try:
            self.conexion = pyodbc.connect(
                f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            )
            self.cursor = self.conexion.cursor()
            print("✅ Conexión exitosa a la base de datos.")
        except Exception as e:
            print("❌ Error de conexión:", e)
            self.conexion = None

    def agregar_banda(self, nombre, total_seguidores=0):
        """ Agrega una nueva banda a la base de datos """
        if self.conexion:
            try:
                query = "INSERT INTO Banda (nombre, total_seguidores) VALUES (?, ?)"
                self.cursor.execute(query, (nombre, total_seguidores))
                self.conexion.commit()
                print(f"🎸 Banda '{nombre}' agregada con éxito.")
            except Exception as e:
                print("❌ Error al agregar banda:", e)

    def agregar_integrante(self, nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id):
        """ Agrega un integrante a la banda """
        if self.conexion:
            try:
                query = """
                INSERT INTO Integrante (nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                self.cursor.execute(query, (nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id))
                self.conexion.commit()
                print(f"🎤 Integrante '{nombre}' agregado con éxito.")
            except Exception as e:
                print("❌ Error al agregar integrante:", e)

    def agregar_concierto(self, fecha, ganancias=0):
        """ Registra un nuevo concierto """
        if self.conexion:
            try:
                query = "INSERT INTO Concierto (fecha, ganancias) VALUES (?, ?)"
                self.cursor.execute(query, (fecha, ganancias))
                self.conexion.commit()
                print(f"🎶 Concierto del {fecha} agregado con éxito.")
            except Exception as e:
                print("❌ Error al agregar concierto:", e)

    def registrar_asistencia(self, integrante_id, concierto_id):
        """ Registra la asistencia de un integrante a un concierto """
        if self.conexion:
            try:
                query = "INSERT INTO Integrante_Concierto (integrante_id, concierto_id) VALUES (?, ?)"
                self.cursor.execute(query, (integrante_id, concierto_id))
                self.conexion.commit()
                print(f"✔ Integrante {integrante_id} registrado en el concierto {concierto_id}.")
            except Exception as e:
                print("❌ Error al registrar asistencia:", e)

    def obtener_integrantes(self):
        """ Obtiene todos los integrantes de la banda """
        if self.conexion:
            try:
                query = "SELECT * FROM Integrante"
                self.cursor.execute(query)
                integrantes = self.cursor.fetchall()
                for integrante in integrantes:
                    print(f"🎼 ID: {integrante[0]}, Nombre: {integrante[1]}, Instrumento: {integrante[2]}, Seguidores: {integrante[4]}")
            except Exception as e:
                print("❌ Error al obtener integrantes:", e)

    def obtener_conciertos(self):
        """ Obtiene todos los conciertos registrados """
        if self.conexion:
            try:
                query = "SELECT * FROM Concierto"
                self.cursor.execute(query)
                conciertos = self.cursor.fetchall()
                for concierto in conciertos:
                    print(f"🎤 ID: {concierto[0]}, Fecha: {concierto[1]}, Ganancias: {concierto[2]}")
            except Exception as e:
                print("❌ Error al obtener conciertos:", e)

    def cerrar_conexion(self):
        """ Cierra la conexión con la base de datos """
        if self.conexion:
            self.conexion.close()
            print("🔌 Conexión cerrada.")


if __name__ == "__main__":
    db = BandaDB()

    if db.conexion:
        while True:
            print("\n📌 Menú de la aplicación:")
            print("1. Agregar banda")
            print("2. Agregar integrante")
            print("3. Agregar concierto")
            print("4. Registrar asistencia")
            print("5. Ver integrantes")
            print("6. Ver conciertos")
            print("7. Salir")

            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                nombre = input("Nombre de la banda: ")
                seguidores = int(input("Total de seguidores: "))
                db.agregar_banda(nombre, seguidores)
            elif opcion == "2":
                nombre = input("Nombre del integrante: ")
                instrumento = input("Instrumento: ")
                imagen = input("Nombre del archivo de imagen: ")
                seguidores = int(input("Número de seguidores: "))
                conciertos = int(input("Número de conciertos: "))
                ganancias = float(input("Ganancias: "))
                banda_id = int(input("ID de la banda: "))
                db.agregar_integrante(nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id)
            elif opcion == "3":
                fecha = input("Fecha del concierto (YYYY-MM-DD): ")
                ganancias = float(input("Ganancias del concierto: "))
                db.agregar_concierto(fecha, ganancias)
            elif opcion == "4":
                integrante_id = int(input("ID del integrante: "))
                concierto_id = int(input("ID del concierto: "))
                db.registrar_asistencia(integrante_id, concierto_id)
            elif opcion == "5":
                db.obtener_integrantes()
            elif opcion == "6":
                db.obtener_conciertos()
            elif opcion == "7":
                db.cerrar_conexion()
                break
            else:
                print("❌ Ingresa una opción válida, por favor.")
