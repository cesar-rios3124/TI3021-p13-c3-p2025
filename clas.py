class Participante:
     def __init__(self, rut: str, nombre: str, edad: int):
          self._rut: str = rut
          self._nombre: str = nombre
          self._edad: int = edad

     def presentarse(self) -> str:
          return f"Hola mi nombre es {self._nombre} y mi edad es {self._edad}"
     
     def __str__(self):
          return f"{self._rut} {self._nombre} {self._edad}"


Participante1 = Participante(
     rut= "19567387-k",
     nombre= "Felipe Villaroel",
     edad= 24
)

Participante2 = Participante(
     rut= "98456276-k",
     nombre="cesar",
     edad= 56
)