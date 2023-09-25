# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests

		
# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()
				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
	puntuación: float = Field(ge=0., lt=5.)
	cuenta: int = Field(ge=1)
				
class Producto(BaseModel):
	_id: Any
	nombre: str
	precio: float
	descripción: str
	categoría: str
	imágen: FilePath | None
	rating: Nota

class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list	


dato = { 
	'nombre': "MBJ Women's Solid Short Sleeve Boat Neck V ", 
	'precio': 9.85, 
	'descripción': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing", 
	'categoría': "women's clothing",
	'imágen': None, 
	'rating': {'puntuación': 4.7, 'cuenta': 130}
}

# Valida con el esquema:
# daría error si no corresponde algún tipo 
producto = Producto(**dato)

print(producto.descripción)
pprint(producto.model_dump()) # Objeto -> python dict


# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  
				
productos_collection.insert_one(producto.model_dump()) 
				
print(productos_collection.count_documents({}))

# todos los productos
lista_productos_ids = []
for prod in productos_collection.find():
	pprint(prod)
	print(prod.get('_id'))   # Autoinsertado por mongo
	lista_productos_ids.append(prod.get('_id'))
	
print(lista_productos_ids)
	
nueva_compra = {
	'usuario': 'fulanito@correo.com',
	'fecha': datetime.now(),
	'productos': lista_productos_ids
}
	
# valida
compra = Compra(**nueva_compra)
pprint(compra.model_dump())
# añade a BD
compras_collection = tienda_db.compras  # Colección
compras_collection.insert_one(compra.model_dump())
	
for com in compras_collection.find():
	pprint(com)
							
productos = getProductos('https://fakestoreapi.com/products')
for p in productos:
	print(p)

# Seleccionamos la base de datos
db = client["base_productos"]
# Coleccion donde insertar productos
coleccion_productos = db["productos"]
# Insertamos los prodcutos
coleccion_productos.insert_many(productos)



print("\n\n\n------------------CONSULTAS------------------")
print("\n\n\nElectrónica entre 100 y 200 euros, ordenados por precio:\n\n")

query1 = {"category": "electronics", "price": {"$lte": 200, "$gte": 100}}
resultado1 = coleccion_productos.find(query1).sort("price",1)

for p in resultado1:
    print(p)

print("\n\n\nProductos que contengas la palabra pocket en la descripción:\n\n")

#Opción i para que no tenga en cuenta mayusculas o minusculas
query2 = {"description" : {"$regex" : "pocket", "$options" : "i"}}
resultado2 = coleccion_productos.find(query2)

for p in resultado2:
	print(p)

print("\n\n\nProductos con puntuación mayor de 4:\n\n")

query3 = {"rating.rate" : {"$gte" : 4}}
resultado3 = coleccion_productos.find(query3)

for p in resultado3:
	print(p)

print("\n\n\nRompa de hombre, ordenada por puntuación:\n\n")

query4 = {"category" : "men's clothing"}
resultado4 = coleccion_productos.find(query4).sort("rating.rate", 1)

for p in resultado4:
	print(p)

print("\n\n\nFacturación total:\n\n")

facturacion = 0
resultado5 = coleccion_productos.find() # Cogemos todos
for p in resultado5:
	precio = p.get("price",0) # Obtener el precio y si no está definido asume 0
	facturacion += precio
print("La facturación total es:", facturacion)

print("\n\n\nFacturación por categoria de producto:\n\n")

# Agrupamos por categoria y sumamos los precios
query6 = [
	{"$group" : {"_id" : "$category","facturacion_total" : {"$sum" : "$price"}}}
]
resultado6 = coleccion_productos.aggregate(query6)

for r in resultado6:
	categoria = r["_id"]
	facturacion = r["facturacion_total"]
	print(f"Categoría: {categoria}, Facturación: {facturacion}")