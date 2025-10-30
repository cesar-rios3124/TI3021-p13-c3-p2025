"""
CRUD
---
Create: Crear un nuevo registro
Read: Leer registro/s
Update: Actualizar registro
Delete: Borrar registro
"""

"""
Glosario
----
* pass
Palabra reservada para que Python no exija el 
codigo minimo necesario para el funcionamiento 
de la funcion/metodo.

* IDE
Viene de la palabra Integrated Development Enviroment
que significa Entorno de desarrollo integrado, que son
los editores de codigo que normalmente utilizamos
para programar en la informatica.

* lint o linter
Es el encargado de vigilar que la sintaxis del 
codigo en el IDE sea correcta y te sugiere
el funcionamiento de este.
"""


# Primero, debemos de crear una clase
from datetime import date
class Persona:
    # Definir cómo se inicializa
    def __init__(
            self,
            rut: int,
            digito_verificador: str,
            nombres: str,
            apellidos: str,
            fecha_nacimiento: date,
            cod_area: int,
            telefono: int
    ):
        self.rut: int = rut
        self.digito_verificador: str = digito_verificador
        self.nombres: str = nombres
        self.apellidos: str = apellidos
        self.fecha_nacimiento: date = fecha_nacimiento
        self.cod_area: int = cod_area
        self.telefono: int = telefono
    
    def _str_(self):
        return f"""
                Rut: {self.rut}-{self.digito_verificador}
                Nombre completo: {self.nombres} {self.apellidos}
                Fecha de nacimiento: {self.fecha_nacimiento}
                Numero de telefono: +{self.cod_area} {self.telefono}
                """       


# Creamos una lista para almacenar varios objetos intanciados de la clase Persona
personas: list[Persona] = []


def persona_existe(nueva_persona: Persona) -> bool:
    for persona in personas:
        if persona.rut == nueva_persona.rut:
            print(f"Persona ya existe con rut: {persona.rut}-{persona.digito_verificador}")
            return True

    print("Persona no existente.")
    return False

def create_persona():
    rut: int = int(input("Ingrese rut sin digito verificador: "))
    digito_verificador: str = input("Ingrese digito verificador: ")
    nombres: str = input("Ingrese nombres de la persona: ")
    apellidos: str = input("Ingrese apellidos de la persona: ")
    dia_nacimiento: int = int(input("Ingrese el dia de nacimiento: "))
    mes_nacimiento: int = int(input("Ingrese el mes de nacimiento: "))
    anio_nacimiento: int = int(input("Ingrese el año de nacimiento: "))
    fecha_nacimiento: date = date(
        year=anio_nacimiento,
        month=mes_nacimiento,
        day=dia_nacimiento
    )
    cod_area: int = int(input("Ingrese codigo de area del numero de telefono: "))
    telefono: int = int(input("Ingrese numero de telefono sin codigo de area: "))

    nueva_persona = Persona(
        rut,
        digito_verificador,
        nombres,
        apellidos,
        fecha_nacimiento,
        cod_area,
        telefono
    )

    if persona_existe(nueva_persona):
        return print("No se registró a la persona.")
    else:
        personas.append(nueva_persona)


def read_persona():
    for persona in personas:
        print("="*20)
        print(persona)
        print("="*20)


def update_persona():
    rut_busqueda =int(input("Ingresa el rut sin digito verificador (EJ: 12345678): "))
    for persona in personas:
        if persona.rut == rut_busqueda:
            while True:
                print(
                    f"""
                    ===========================
                    ||  Edición de personas  ||
                    ===========================
                    1. Rut: {persona.rut}
                    2. Diguto verificador: {persona.digito_verificador}
                    3. Nombres: {persona.nombres}
                    4. Apellido: {persona.apellidos}
                    5. Fecha de nacimiento: {persona.fecha_nacimiento}
                    6. Codigo de area: {persona.cod_area}
                    7. Telefono: {persona.telefono}
                    0. No seguir modificando.
                    """
                )
                opcion =input("¿Que dato quieres modificar?")
                if opcion == "1":
                    rut: int = int(input("Ingresa el rut de la persona: "))
                    for persona in personas:
                        if persona.rut == rut:
                            print(f"La persona con el rut {persona.rut} ya existe. Intente con otro rut. ")
                        else:
                            persona.rut = rut
                            print("Rut modificado exitosamente ")
                elif opcion == "2":
                    digito_verificador: str = input("Ingresa el digito verificador : ")
                    persona.digito_verificador = digito_verificador
                    print("Digito verificador modificado exitosamente ")

                elif opcion == "3":
                    nombres: str = input("Ingresa los nombres de la persona: ")
                    persona.nombres =nombres
                    print("Nombres modificado exitosamente ")
                
                elif opcion == "4":
                    apellidos: str = input("Ingrsa los apellidos de la persona: ")
                    persona.apellidos = apellidos
                    print("Nombres modificado exitosamente ")

                elif opcion == "5":
                    dia_nacimiento = int(input("Ingresa el dia de nacimiento de la persona: "))
                    mes_nacimiento = int(input("Ingresa el mes de nacimiento de la persona: "))
                    anio_nacimiento = int(input(" Ingresa el año de nacimiento de la persona: "))
                    fecha_nacimiento: date = date(
                        year=anio_nacimiento,
                        month=mes_nacimiento,
                        day=dia_nacimiento
                    )
                    persona.fecha_nacimiento = fecha_nacimiento
                    print("Fecha de nacimiento modificado exitosamente ")

                elif opcion == "6":
                    cod_area: int = int(input("Ingresa el codigo de area del telefono de la persona: "))
                           

    


def delete_persona():
    pass

create_persona()
print(personas)