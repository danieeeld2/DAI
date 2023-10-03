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

### Copia de seguridad usando mongodump accediendo al contenedor

Para hacer la copia de seguridad de la base de datos, primero debemos acceder al contenedor, que en nuestro caso se llama `dai-mongo-1`. Para ello, ejecutamos:

```bash
docker exec -it dai-mongo-1 bash
```
Ahora ejecutamos ```mongodump``` para hacer la copia de seguridad. Con el parámetro `--out` podemos decidir la ubicación de la copia:

```bash
mongodump --out /backup
```
Esto creará una copia de seguridad dentro de la carpeta `/backup`. Ahora podemos salir del contenedor usando `exit` y hacer una copia fuera del contenedor usando:

```bash
docker cp dai-mongo-1:/backup RUTA_DESTINO_EN_EL_SISTEMA_ANFITRIÓN
```

### Copia de seguridad usando mongodump desde el host

Primero tenemos que asegurarnos de que la carpeta compartida está configurada en el sistema host (Esto implica que debes tener una carpeta en tu sistema host que esté mapeada a una ubicación dentro del contenedor de MongoDB). En nuestro caso, tenemos la carpeta `e-comerce`.

Ejecutamos el contenedor y desde nuestro sistema host llamamos a `mongodump` para crear la copia de seguridad y guardarla en la compartida:

```bash
mongodump --host NOMBRE_DEL_HOST --port PUERTO_MONGO --out RUTA_DE_LA_CARPETA_COMPARTIDA
```
En nuestro caso `host=localhost`, por lo que...