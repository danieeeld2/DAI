# DAI

Repositorio para las prácticas de DAI

### Iniciar contenedor docker

```bash
docker compose run app Seed.py
```

### Detener contenedor docker

```bash
docker compose down
```
### Copia de seguridad usando mongodump desde el host

Primero tenemos que asegurarnos de que la carpeta compartida está configurada en el sistema host (Esto implica que debes tener una carpeta en tu sistema host que esté mapeada a una ubicación dentro del contenedor de MongoDB). En nuestro caso, tenemos la carpeta `e-comerce`.

Ejecutamos el contenedor y desde nuestro sistema host llamamos a `mongodump` para crear la copia de seguridad y guardarla en la compartida:

```bash
sudo docker compose run mongo mongodump --host mongo --port 27017 --db tienda --out backup/
```
Para que funcione he cambiado el `docker-compose.yml`, añadiendo la línea `- ./backup:/backup` y tras hacer `docker compose up`  le he dado privilegios a la carpeta con `sudo chmod o+w backup/`

