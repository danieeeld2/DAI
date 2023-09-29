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

# Le pasas una coleccion de compras
def calc_facturacion(collection):
	ids_cant = []	# Almacenará pares de idintificadores y cantidades
	for c in collection:
		pr = c.get("products")	# Obtenemos la lista de productos comprados de cada compra
		for p in pr:
			ids_cant.append([p.get("productID"),p.get("quantity")])
	
	facturacion = 0
	pr_coll = productos_collection.find()
	for id in ids_cant:
		# Para cada par se busca el producto correspondiente en la coleccion de productos usando el
		# identificador de producto id[0] y se toma el primero que es [0]
		# porque entendemos que el identificador es único
		prod = pr_coll.collection.find({"id":id[0]})[0]
		facturacion += prod.get("price")*id[1] # Cantidad comprada por precio

	return round(facturacion,2)
				
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


# dato = { 
# 	'nombre': "MBJ Women's Solid Short Sleeve Boat Neck V ", 
# 	'precio': 9.85, 
# 	'descripción': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing", 
# 	'categoría': "women's clothing",
# 	'imágen': None, 
# 	'rating': {'puntuación': 4.7, 'cuenta': 130}
# }

# Valida con el esquema:
# daría error si no corresponde algún tipo 
# producto = Producto(**dato)

# print(producto.descripción)
# pprint(producto.model_dump()) # Objeto -> python dict


# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  

# Vaciamos antes de añadir
productos_collection.drop()
				
# productos_collection.insert_one(producto.model_dump()) 

# Insertamos todos los productos
productos = getProductos('https://fakestoreapi.com/products')
productos_collection.insert_many(productos)
				
print(productos_collection.count_documents({}))

# # todos los productos
# lista_productos_ids = []
# for prod in productos_collection.find():
# 	pprint(prod)
# 	print(prod.get('_id'))   # Autoinsertado por mongo
# 	lista_productos_ids.append(prod.get('_id'))
	
# print(lista_productos_ids)
	
# nueva_compra = {
# 	'usuario': 'fulanito@correo.com',
# 	'fecha': datetime.now(),
# 	'productos': lista_productos_ids
# }
	
# # valida
# compra = Compra(**nueva_compra)
# pprint(compra.model_dump())

# añade a BD

compras_collection = tienda_db.compras  # Colección
# compras_collection.insert_one(compra.model_dump())

# Vaciamos antes de añadir
compras_collection.drop()

# Insertamos todos las compras
compras = getProductos('https://fakestoreapi.com/carts')
compras_collection.insert_many(compras)


	
# for com in compras_collection.find():
# 	pprint(com)
							
# productos = getProductos('https://fakestoreapi.com/products')
# for p in productos:
# 	print(p)

# # Seleccionamos la base de datos
# db = client["base_productos"]
# # Coleccion donde insertar productos
# coleccion_productos = db["productos"]
# # Insertamos los prodcutos
# coleccion_productos.insert_many(productos)



print("\n\n\n------------------CONSULTAS------------------")
print("\n\n\nElectrónica entre 100 y 200 euros, ordenados por precio:\n\n")

query1 = {"category": "electronics", "price": {"$lte": 200, "$gte": 100}}
resultado1 = productos_collection.find(query1).sort("price",1)

for p in resultado1:
    pprint(p)

print("\n\n\nProductos que contengas la palabra pocket en la descripción:\n\n")

#Opción i para que no tenga en cuenta mayusculas o minusculas
query2 = {"description" : {"$regex" : "pocket", "$options" : "i"}}
resultado2 = productos_collection.find(query2)

for p in resultado2:
	pprint(p)

print("\n\n\nProductos con puntuación mayor de 4:\n\n")

query3 = {"rating.rate" : {"$gte" : 4}}
resultado3 = productos_collection.find(query3)

for p in resultado3:
	pprint(p)

print("\n\n\nRompa de hombre, ordenada por puntuación:\n\n")

query4 = {"category" : "men's clothing"}
resultado4 = productos_collection.find(query4).sort("rating.rate", 1)

for p in resultado4:
	pprint(p)

print("\n\n\nFacturación total:\n\n")

ids_cant = []
for c in compras_collection.find():
	pr = c.get("products")
	for p in pr:
		ids_cant.append([p.get("productId"),p.get("quantity")])
facturacion = 0
pr_coll = productos_collection.find()
for id in ids_cant:
	prod = pr_coll.collection.find({"id":id[0]})[0]
	facturacion += prod.get("price")*id[1]

print(str(round(facturacion,2))+"€")

print("\n\n\nFacturación por categoria de producto:\n\n")

categories = []
# Hacemos una lista de las categorias
for record in productos_collection.find():
	cat=record.get("category")
	if cat not in categories:
		categories.append(cat)
for cat in categories:
	print('\n  ' + cat)
	facturacion = 0
	coll = productos_collection.find({"category":cat})
	for p in coll:
		for id in ids_cant:
			# Vemos si coincide el id
			if p.get("id") == id[0]:
				facturacion += p.get("price")*id[1]

	print(str(round(facturacion,2))+"€")