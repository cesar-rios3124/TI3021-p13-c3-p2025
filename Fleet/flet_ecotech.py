from ecotech import Auth, Database, Finance
from dotenv import load_dotenv
import flet as ft 
import os 

load_dotenv()

class App:
    def __init__(self, page: ft.Page):
        self,page = page
        self.page.ticle = "Ecotech Solutions"
        self.db = Database(
            username=os.getenv("OEACLE_USER")
            password=os.g("OARCLE_PASSWORD")
            dsn=os.getenv("ORACLE_DSN")
        )


    def page_register(self):
        self.page.controls.clear()

        self.input_id = ft.TextField(
            label=" ID del usuarios",
            hint_text="INGRESE un nombre de usuario"
        )

        

    def page_register(self):
        self.page.controls.clear()
        #Codigo
        self.page_update()

    def page_login(self):
        self.page.controls.clear()
        #Codigo
        self.page_update()
    
    def page_main_menu(self):
        self.page.controls.clear()
        #Codigo
        self.page_update()

    def page_indicator_menu(self):
        self.page.controls.clear()
        #Codigo
        self.page_update()            

    def page_history_menu(self):
        self.page.controls.clear()
        #Codigo
        self.page_update()