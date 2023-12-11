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
