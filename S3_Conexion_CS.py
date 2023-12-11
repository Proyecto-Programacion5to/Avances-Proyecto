import pandas as pd
from mysql.connector import connect, Error
import mysql.connector
from PF_ArchivoConstantes_CS import data_limpieza, host, user, password, data_classification, data_query1, data_query2

#REALIZAR CONEXION CON LA BASE DE DATOS
class DataBaseProyecto:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conexión exitosa a MySQL.")
            else:
                print("No se pudo establecer la conexión.")

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos:", error)

    def crear_base_datos(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS Proyecto_Programacion")
            print("Base de datos creada o ya existente.")

        except mysql.connector.Error as error:
            print("Error al crear la base de datos:", error)

    def crear_tablas(self):
        try:
            tablas = [
                """
                USE Proyecto_Programacion
                """,
                """
                CREATE TABLE IF NOT EXISTS Clasificaciones (
                IdClas INT PRIMARY KEY,
                Clasificacion VARCHAR(200)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Productos (
                  IdProduct INT PRIMARY KEY,
                  IdClas INT NOT NULL,
                  Producto VARCHAR(1000),
                  FOREIGN KEY (IdClas) REFERENCES Clasificaciones(IdClas)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Precios (
                  IdProduct INT PRIMARY KEY,
                  Precio_Actual DECIMAL(10, 2),
                  Precio_Anterior DECIMAL(10, 2),
                  FOREIGN KEY (IdProduct) REFERENCES Productos(IdProduct)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Pago_por_Producto (
                  IdProduct INT PRIMARY KEY,
                  Pago_Mensual DECIMAL(10, 2),
                  FOREIGN KEY (IdProduct) REFERENCES Productos(IdProduct)
                )
                """
            ]

            for tabla in tablas:
                self.cursor.execute(tabla)
                print("Tabla creada exitosamente.")

        except mysql.connector.Error as error:
            print("Error al crear las tablas:", error)

    def insertar_datos(self):
        df = pd.read_csv(data_limpieza, index_col=0)
        try:
            data_clasificacion = df.Clasificacion.unique()
            data_clasificacion = pd.DataFrame(data_clasificacion)
            data_clasificacion.columns = ['Clasificacion']
            data_clasificacion.to_csv(data_classification, index=True)
            data_clas = pd.read_csv(data_classification, index_col=0)

            # Crear un diccionario que mapea nombres de clasificación a sus IDs
            id_clasificacion = dict(zip(data_clas['Clasificacion'], data_clas.index))

            for index, row in data_clas.iterrows():
                insertardatos = """
                           insert into Clasificaciones (IdClas, Clasificacion) values (%s, %s)
                           """
                self.cursor.execute(
                    insertardatos, (index, row['Clasificacion'])
                )

            for index, row in df.iterrows():
                id_clas = id_clasificacion.get(row['Clasificacion'])
                if id_clas is not None:
                    insertardatos = """
                               insert into Productos (IdProduct, IdClas, Producto) values (%s, %s, %s)
                               """
                    self.cursor.execute(
                        insertardatos, (index, id_clas, row['Producto'])
                    )
                else:
                    print(f"No se encontró la clasificación para el producto: {row['Producto']}")

            for index, row in df.iterrows():
                insertardatos = """
                           insert into Precios (IdProduct, Precio_Actual, Precio_Anterior)
                           values (%s, %s, %s)
                           """
                self.cursor.execute(
                    insertardatos, (index, row['Precio Actual'], row['Precio Anterior'])
                )

            for index, row in df.iterrows():
                insertardatos = """
                           insert into Pago_por_Producto (IdProduct, Pago_Mensual)
                           values (%s, %s)
                           """
                self.cursor.execute(
                    insertardatos, (index, row['Pago Mensual'])
                )

            self.connection.commit()
            print("Datos insertados correctamente en las tablas creadas anteriormente.")

        except (mysql.connector.Error, pd.errors.EmptyDataError) as error:
            print("Error al insertar datos considerados:", error)

    def crearquerys(self):
        try:
            self.cursor.execute("USE Proyecto_Programacion")

            # QUERY 1
            query1 = ("SELECT p.IdClas, c.Clasificacion, COUNT(p.IdClas) FROM productos p "
                      "JOIN clasificaciones c ON p.IdClas = c.IdClas "
                      "GROUP BY p.IdClas, c.Clasificacion")
            self.cursor.execute(query1)
            resultado = self.cursor.fetchall()

            dfquery1 = pd.DataFrame(resultado, columns=['IdClasificacion', 'Clasificacion', 'Cantidad'])
            dfquery1 = dfquery1.set_index("IdClasificacion", drop=True)
            dfquery1.to_csv(data_query1)
            # print(dfquery1)

            # QUERY 2
            dfquery2 = ("SELECT c.Clasificacion AS Clasificacion, pd.Producto AS Producto, "
                        "(p.Precio_Anterior - p.Precio_Actual) AS Descuento "
                        "FROM precios p "
                        "JOIN productos pd ON p.IdProduct = pd.IdProduct "
                        "JOIN clasificaciones c ON pd.IdClas = c.IdClas")
            self.cursor.execute(dfquery2)
            resultado = self.cursor.fetchall()

            dfquery2 = pd.DataFrame(resultado, columns=['Clsificacion', 'Producto', 'Descuento'])
            dfquery2.to_csv(data_query2)
            # print(dfquery2)

        except mysql.connector.Error as error:
            print("Error al ejecutar las consultas:", error)

    def cerrar_conexion(self):
        self.cursor.close()
        self.connection.close()

    # if __name__ == "__main__":