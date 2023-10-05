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

```bash
sudo docker compose run mongo mongodump --host mongo --port 27017 --db tienda --out backup/
```
Para que funcione he cambiado el `docker-compose.yml`, añadiendo la línea `- ./backup:/backup` y tras hacer `docker compose up`  le he dado privilegios a la carpeta con `sudo chmod o+w backup/`

