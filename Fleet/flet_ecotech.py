from ecotech import Auth, Database, Finance
from dotenv import load_dotenv
import flet as ft
import os
import datetime

load_dotenv()


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ecotech Solutions"

        self.db = Database(
            username=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )

        try:
            self.db.create_all_tables()
        except Exception as error:
            print(f"{error}")

        self.loged_user = ""
        self.page_register()

    # REGISTRO

    def page_register(self):
        self.page.controls.clear()

        self.input_id = ft.TextField(label="ID del usuario")
        self.input_username = ft.TextField(label="Nombre de usuario")
        self.input_password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True
        )

        self.button_register = ft.Button(
            text="Registrarse",
            on_click=self.handle_register
        )

        self.text_status = ft.Text("")
        self.button_login = ft.Button(
            text="Inicia sesión",
            on_click=lambda e: self.page_login()
        )

        self.page.add(
            self.input_id,
            self.input_username,
            self.input_password,
            self.button_register,
            self.text_status,
            self.button_login
        )

        self.page.update()

    def handle_register(self, e):
        try:
            id_user = int(self.input_id.value)
            status = Auth.register(
                db=self.db,
                id=id_user,
                username=self.input_username.value.strip(),
                password=self.input_password.value.strip()
            )
            self.text_status.value = status["message"]
        except ValueError:
            self.text_status.value = "El ID debe ser numérico"

        self.page.update()

    # LOGIN

    def page_login(self):
        self.page.controls.clear()

        self.input_username = ft.TextField(label="Usuario")
        self.input_password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True
        )

        self.button_login = ft.Button(
            text="Iniciar sesión",
            on_click=self.handle_login
        )

        self.text_status = ft.Text("")
        self.button_register = ft.Button(
            text="Registrarse",
            on_click=lambda e: self.page_register()
        )

        self.page.add(
            self.input_username,
            self.input_password,
            self.button_login,
            self.text_status,
            self.button_register
        )

        self.page.update()

    def handle_login(self, e):
        status = Auth.login(
            db=self.db,
            username=self.input_username.value.strip(),
            password=self.input_password.value.strip()
        )

        self.text_status.value = status["message"]
        self.page.update()

        if status["success"]:
            self.loged_user = self.input_username.value.strip()
            self.page_main_menu()

    # MENU PRINCIPAL

    def page_main_menu(self):
        self.page.controls.clear()

        self.page.add(
            ft.Text("Main Menu", size=32, weight=ft.FontWeight.BOLD),
            ft.Text(f"Hola {self.loged_user}"),
            ft.Button("Consultar Indicadores", on_click=lambda e: self.page_indicator_menu()),
            ft.Button("Historial de consultas", on_click=lambda e: self.page_history_menu()),
            ft.Button("Cerrar sesión", on_click=lambda e: self.page_login())
        )

        self.page.update()

    # CONSULTA DE INDICADORES

    def page_indicator_menu(self):
        self.page.controls.clear()

        self.dropdown_indicator = ft.Dropdown(
            label="Indicador económico",
            options=[
                ft.dropdown.Option("dolar"),
                ft.dropdown.Option("uf"),
                ft.dropdown.Option("utm")
            ]
        )

        self.input_date = ft.TextField(
            label="Fecha (YYYY-MM-DD o DD-MM-YYYY)"
        )

        self.text_result = ft.Text("")
        self.button_consult = ft.Button(
            text="Consultar",
            on_click=self.handle_indicator_consult
        )

        self.button_back = ft.Button(
            text="Volver",
            on_click=lambda e: self.page_main_menu()
        )

        self.page.add(
            self.dropdown_indicator,
            self.input_date,
            self.button_consult,
            self.text_result,
            self.button_back
        )

        self.page.update()

    def handle_indicator_consult(self, e):
        indicator = self.dropdown_indicator.value
        raw_date = self.input_date.value.strip()

        if not indicator or not raw_date:
            self.text_result.value = "Debe seleccionar indicador y fecha"
            self.page.update()
            return

        # ACEPTA AMBOS FORMATOS

        fecha_obj = None
        for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                fecha_obj = datetime.datetime.strptime(raw_date, fmt)
                break
            except ValueError:
                pass

        if not fecha_obj:
            self.text_result.value = "Fecha inválida. Use YYYY-MM-DD o DD-MM-YYYY"
            self.page.update()
            return

        api_date = fecha_obj.strftime("%d-%m-%Y")

        try:
            result = Finance.get_indicator(
                indicator=indicator,
                date=api_date
            )

            if not result or result.get("value") is None:
                self.text_result.value = "No hay datos para esa fecha"
                self.page.update()
                return

            self.text_result.value = (
                f"Indicador: {indicator}\n"
                f"Fecha: {api_date}\n"
                f"Valor: {result['value']}\n"
                f"Fuente: {result['source']}"
            )

            self.db.save_query(
                user=self.loged_user,
                indicator=indicator,
                date=api_date,
                value=result["value"],
                source=result["source"]
            )

        except Exception as error:
            self.text_result.value = f"Error API: {error}"

        self.page.update()

    # HISTORIAL

    def page_history_menu(self):
        self.page.controls.clear()

        history = self.db.get_user_history(self.loged_user)
        list_view = ft.ListView(expand=True)

        for item in history:
            list_view.controls.append(
                ft.Text(
                    f"{item['indicator']} | "
                    f"Fecha: {item['date']} | "
                    f"Valor: {item['value']} | "
                    f"{item['created_at']} | "
                    f"{item['source']}"
                )
            )

        self.page.add(
            list_view,
            ft.Button("Volver", on_click=lambda e: self.page_main_menu())
        )

        self.page.update()


if __name__ == "__main__":
    ft.app(target=App)
