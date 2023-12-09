from django.db import models
from pymongo import MongoClient
from pydantic import BaseModel, Field, FilePath #field_validator
from typing import Any
from bson.objectid import ObjectId
from bson.json_util import dumps
import logging

logger = logging.getLogger(__name__)

# Quitamos el field_validator porque no funciona con el ninja

# Create your models here.
class Rating(BaseModel):
	rate: float = Field(ge=0., lt=5.)
	count: int = Field(ge=1)
class Producto(BaseModel):
	id: Any
	title: str
	price: float
	description: str
	category: str
	image: FilePath | None

	# @field_validator('title')
	@classmethod
	def title_mayuscula(cls,v):
		if v[0].islower():
			raise ValueError('El título debe empezar por mayúscula')
		return v.title()

# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  
compras_collection = tienda_db.compras  # Colección

def ObtenerProductos():
    resultado = productos_collection.find()
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ObtenerProductosId(id):
    resultado = productos_collection.find({"_id": ObjectId(id)})
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ObtenerProductosConcretos(query):
    resultado = productos_collection.find({"$or": [{"title": {"$regex": query, "$options": "i"}}, {"description": {"$regex": query, "$options": "i"}}]})
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ObtenerProductosCategoria(categoria):
    resultado = productos_collection.find({"category": categoria})
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def EliminarProducto(id):
    try:
        resul = productos_collection.find({"_id": ObjectId(id)})
        resultado = {}
        for attr, val in resul[0].items():
            if attr == "_id":
                resultado["id"] = str(val)
            else:
                resultado[attr] = val
        logger.debug(f'{resultado}')
        productos_collection.delete_one({"_id": ObjectId(id)})
        return resultado
    except Exception as e:
        logger.error(e)
        logger.error("Error al eliminar el producto")        
        return False

def ModificarProducto(id, atributo, valor):
    try:
        productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {atributo: valor}})
        return True
    except Exception as e:
        logger.error(e)
        logger.error("Error al modificar el producto")        
        return False
    
def handle_uploaded_file(f):
    directorio_destino = "static/imagenes/" 
    directorio_imagenes = "imagenes/"
    nombre_archivo = f.name.split('/')[-1]
    nombre_archivo_destino = directorio_imagenes+nombre_archivo
    ruta_archivo_destino = directorio_destino+nombre_archivo
    with open(ruta_archivo_destino,"wb") as archivo:
        archivo.write(f.read())
    with open(nombre_archivo_destino,"wb") as archivo:
        archivo.write(f.read())
    return nombre_archivo_destino
    
def CrearProducto(title, price, description, category, image):
    try:
        image = handle_uploaded_file(image)
        producto = {"title": title, "price": price, "description": description, "category": category, "image": image, "rating": {"count": 0, "rate": 0}}
        insertado = productos_collection.insert_one(producto)
        resultado = productos_collection.find({"_id": insertado.inserted_id})
        resultado = list(resultado)
        for r in resultado:
            r["id"] = str(r.get("_id"))
            del r["_id"]
        return resultado
    except Exception as e:
        logger.error(e)
        logger.error("Error al crear el producto")        
        return False

def ObtenerCategorias():
    categorias = []
    for record in productos_collection.find():
        cat=record.get("category")
        if cat not in categorias:
            categorias.append(cat)
    return categorias

def AñadirProducto(producto):
    try:
        productos_collection.insert_one(producto)
    except Exception as e:
        print(e)
        print("Error al añadir el producto")
        return False

def ModificarRating(id, rate):
    try:
        product = productos_collection.find_one({"_id": ObjectId(id)})
        if product:
            new_rating = Rating(**product["rating"])
            new_count = new_rating.count + 1
            new_rate = ((new_rating.rate * new_rating.count) + (rate * 1.0)) / new_count
            productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"rating": {"count": new_count, "rate": new_rate}}})
            return ObtenerProductosId(id)
    except Exception as e:
        logger.error(e)
        logger.error("Error al modificar el rating")        
        return False

#######################################################################################

def consulta1():
    query1 = {"category": "electronics", "price": {"$lte": 200, "$gte": 100}}
    resultado1 = productos_collection.find(query1).sort("price",1)
    resultado = " ".join([str(x) for x in resultado1])
    return resultado

def consulta2():
    query2 = {"description" : {"$regex" : "pocket", "$options" : "i"}}
    resultado2 = productos_collection.find(query2)
    resultado = " ".join([str(x) for x in resultado2])
    return resultado

def consulta3():
    query3 = {"rating.rate" : {"$gte" : 4}}
    resultado3 = productos_collection.find(query3)
    resultado = " ".join([str(x) for x in resultado3])
    return resultado

def consulta4():
    query4 = {"category" : "men's clothing"}
    resultado4 = productos_collection.find(query4).sort("rating.rate", 1)
    resultado = " ".join([str(x) for x in resultado4])
    return resultado

# def consulta5():
#     ids_cant = []
#     for c in compras_collection.find():
#         pr = c.get("products")
#         for p in pr:
#             ids_cant.append([p.get("productId"),p.get("quantity")])
#     facturacion = 0
#     pr_coll = productos_collection.find()
#     for id in ids_cant:
#         prod = pr_coll.collection.find({"id":id[0]})[0]
#         facturacion += prod.get("price")*id[1]
#     return str(facturacion)

# def consulta6():
#     categories = []
#     ids_cant = []
#     resultado = []
#     for c in compras_collection.find():
#         pr = c.get("products")
#         for p in pr:
#             ids_cant.append([p.get("productId"),p.get("quantity")])
#     for record in productos_collection.find():
#         cat=record.get("category")
#         if cat not in categories:
#             categories.append(cat)
#     for cat in categories:
#         facturacion = 0
#         coll = productos_collection.find({"category":cat})
#         for p in coll:
#             for id in ids_cant:
#                 if p.get("id") == id[0]:
#                     facturacion += p.get("price")*id[1]
#         resultado.append([cat,facturacion])
#     resultado_final = " ".join([str(x) for x in resultado])
#     return resultado_final
 

