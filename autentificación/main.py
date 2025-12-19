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
        hashed_password = bcrypt.hashpw(password, salt)
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
            password_user = usuario[2]
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


# ============================
# MENÚ DE USUARIO (AGREGADO)
# ============================

def menu_principal():
    db = Database(username, password, dsn)
    finance = Finance()

    while True:
        print("\n====== MENÚ PRINCIPAL ======")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Consultar indicador")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            user = input("Ingrese usuario: ")
            pwd = input("Ingrese contraseña: ")
            auth.register(db, user, pwd.encode())
            print("Usuario registrado.")

        elif opcion == "2":
            user = input("Usuario: ")
            pwd = input("Contraseña: ")

            if auth.login(db, user, pwd.encode()):
                print("Sesión iniciada correctamente.")
                menu_usuario(finance)
            else:
                print("Credenciales incorrectas.")

        elif opcion == "3":
            indicador = input("Ingrese indicador (uf, ivp, ipc, utm, dolar, euro): ")
            finance.gert_indicator(indicador)

        elif opcion == "4":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


def menu_usuario(finance: Finance):
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1. Ver UF")
        print("2. Ver dolar")
        print("3. Ver euro")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            finance.gert_indicator("uf")
        elif opcion == "2":
            finance.gert_indicator("dolar")
        elif opcion == "3":
            finance.gert_indicator("euro")
        elif opcion == "4":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    indicadores = Finance()
    
    menu_principal()
