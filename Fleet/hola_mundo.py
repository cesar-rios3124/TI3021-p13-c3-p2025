#
import flet as ft

#
class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola mundo"
        # Siempre como ultima linea de __init__
        self.build()
        # Metodo de aplicación para agregar elementos 
        # En mi paguina/aplicacion
    def build(self):
        self.page.add(
            ft.Text(value="Hola mundo")
        )
#
if __name__ == "__main__":
    ft.app(target=App)
