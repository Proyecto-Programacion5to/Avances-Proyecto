import pandas as pd
import re

class LimpiadorCSV:
    def __init__(self, archivo):
        self.df = pd.read_csv(archivo)

    def limpieza_duplicados(self):
        self.df = self.df.drop_duplicates()

    def limpieza_nulos(self):
        self.df = self.df.dropna()

    def limpieza_de_precio(self):
        def limpiar_precio(valor):
            if isinstance(valor, str):
                valor = valor.replace('MXN', '').strip()
                partes = valor.split('.')
                if len(partes) > 1:
                    valor = partes[0] + partes[1]
                valor = valor.replace('$', '').replace(',', '').strip()
                return float(valor)
            return valor
        self.df['Precio Actual'] = self.df['Precio Actual'].apply(limpiar_precio)
        self.df['Precio Anterior'] = self.df['Precio Anterior'].apply(limpiar_precio)

    def extraer_valores_numericos(self, columna):
        def obtener_valor_numerico(celda):
            conjunto = re.findall(r'\b(\d+)\b', str(celda))
            return int(conjunto[0]) if conjunto else None
        self.df[columna] = self.df[columna].apply(obtener_valor_numerico)

    def signo_de_pesos(self):
        self.df['Forma de pago'] = self.df['Forma de pago'].astype(str).str.replace('$', '')

    def limpiar_forma_de_pago(self):
        def lipieza_formaspago(valor):
            if isinstance(valor, str):
                valor = valor.replace(',', '').strip()
                return float(valor)
            return valor
        self.df['Forma de pago'] = self.df['Forma de pago'].apply(lipieza_formaspago)

    def guardar_csv(self, archivo_salida):
        self.df.to_csv(archivo_salida, index=False)


archivo_csv = 'Datasets/ClaroShop.csv'
limpieza = LimpiadorCSV(archivo_csv)
limpieza.limpieza_duplicados()
limpieza.limpieza_nulos()
limpieza.limpieza_de_precio()
limpieza.extraer_valores_numericos('Forma de pago')
limpieza.limpiar_forma_de_pago()
limpieza.signo_de_pesos()
limpieza.guardar_csv('Limpieza_ClaroShop.csv')
