from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema, Query, Form
from .import models
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging
from typing import List
from ninja.security import HttpBearer


logger = logging.getLogger(__name__)

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "DAI2023":
            return token

api = NinjaExtraAPI(auth=GlobalAuth())

class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):  # sirve para validar y para documentación
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema):
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str
	
@api.get('/products', response = {202: List[ProductSchema]})
def Productos(request, since: int = Query(default=0), to: int = Query(default=4)):
	resultados = models.ObtenerProductos()[since:to]
	return 202, list(resultados)

@api.put("/productos/{id}", response = {202: ProductSchema, 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn = Form(...)):
	try:
		for attr, value in payload.dict().items():
			logger.debug(f'{attr} -> {value}')
			models.ModificarProducto(id, attr, value)
		payload["id"] = id
		logger.debug(f'{payload}')
		return 202, payload
	except:
		return 404, {'message': 'no encontrado'}

@api.get('/products/{id}', response={200 : List[ProductSchema], 404 : ErrorSchema})
def ProductosId(request, id : str):
	try:
		resultado = models.ObtenerProductosId(id)
		return 200, list(resultado)
	except Exception as e:
		logger.error(e)
		return 404, {"message": "No se ha encontrado el producto"}
	
@api.delete('/products/{id}', response={200 :ProductSchema, 404 : ErrorSchema})
def EliminarProducto(request, id : str):
	try:
		resultado = models.EliminarProducto(id)
		return 200, resultado
	except Exception as e:
		logger.error(e)
		return 404, {"message": "No se ha encontrado el producto"}

@api.post('/products', response={201 : List[ProductSchema], 400 : ErrorSchema})
def CrearProducto(request, payload : ProductSchemaIn=Form(...)):
	try:
		resultado = models.CrearProducto(payload)
		return 201, list(resultado)
	except Exception as e:
		logger.error(e)
		return 400, {"message": "No se ha podido crear el producto"}
	
@api.post("/token", auth=None) 
def get_token(request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "DAI2324":
        return {"token": "DAI2023"}