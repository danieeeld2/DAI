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

### Copia de seguridad usando mongodump

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


