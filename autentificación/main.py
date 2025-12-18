# Conectarnos a la base de datos
import oracledb
# Rescatar variables de entorno
import os
from dotenv import load_dotenv
# Implementar hasheo de contraseñas
import bcrypt
#Importar el tipo de dato Opcional
from typing import Optional
# Implementar peticiones HTTP
import requests
# Importar liberia de fecha
import datetime
# Cargar las variables desde el archivo .env
load_dotenv()
# Rescatar las credenciales de conexión con Oracle
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self, username, password, dsn):
        self.username = username 
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        pass
    def query(self,sentence: str, parameters: Optional[dict] =None):
        print(f"Ejecutando query:\n{sentence}\nParametros:\n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    resultado = cursor.execute(sentence, parameters)
                    return resultado
                connection.commit()
        except oracledb.DatabaseError as error:
            print (f"hubo un error con la base de datos :\n {error}")


# Generar aunteficación
class auth:
    @staticmethod
    def register(db: Database, username: str, password: str):
        salt  = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(password,salt)
        usuario = {
            "id": 1,
            "username": username, 
            "password": hashed_password
        }

        db.query(
            "INSERT INTO USERS(id,username,password) values (:id,:username:password)",
            usuario
        )
    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
        resultado = db.query(
            "SELECT * FROM USERS WHERE username = :username",
            {"username": username}
        )  

        for usuario in resultado:
            password_user =usuario[2]
            return bcrypt.checkpw(password, password_user)

class Finance: 
    def __init__(self, base_url:str = "https://mindicador.cl/api"):
        self.base_url =  base_url
    def gert_indicator(self,indicator: str = None, fecha:str=None):
        if not indicator:
            return print("Indicator faltante")
        if not fecha:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            fecha =f"{day}-{month}-{year}"
        url = f"{self.base_url}/{indicator}/{fecha}"
        data = requests.get(url=url).json()
        print(data['serie'][0]['valor'])
    def gert_uf(self,fecha: str = None):
        self.gert_indicator("uf", fecha)
    def gert_uf(self,fecha: str = None):
        self.gert_indicator("ivp", fecha)
    def gert_uf(self,fecha: str = None):
        self.gert_indicator("ipc", fecha)
    def gert_uf(self,fecha: str = None):
        self.gert_indicator("utm", fecha)
    def gert_uf(self,fecha: str = None):
        self.gert_indicator("dolar", fecha)
    def gert_uf(self,fecha: str = None):
        self.gert_indicator("euro", fecha)

if __name__ == "__main__":
    indicadores = Finance()
    indicadores.get_euro()