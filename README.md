## Instalar Docker

* Mac, Windows y Ubuntu: [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Docker Desktop Documentation](https://docs.docker.com/desktop/)

### Revisar si el puerto 80 está ocupado. 

Debian:
```bash
netstat -tulpn | grep 80
```
Mac:
```bash
sudo lsof -i :80
```
```bash
docker-compose build
docker-compose up
docker-compose ps

    Name                  Command               State                    Ports                  
------------------------------------------------------------------------------------------------
test_nginx_1   /docker-entrypoint.sh ngin ...   Up      0.0.0.0:80->80/tcp,:::80->80/tcp        
test_web_1     python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
```

```bash
docker exec test_web_1  python manage.py  makemigrations rapihogar
docker exec test_web_1  python manage.py  migrate
```
### Cargar datos de pruebas
```bash
docker exec test_web_1 python manage.py loaddata rapihogar/fixtures/user.json --app rapihogar.user
docker exec test_web_1 python manage.py loaddata rapihogar/fixtures/company.json --app rapihogar.company
docker exec test_web_1 python manage.py loaddata rapihogar/fixtures/scheme.json --app rapihogar.scheme
docker exec test_web_1 python manage.py loaddata rapihogar/fixtures/pedido.json --app rapihogar.pedido
```

```bash
docker exec -it test_web_1 python manage.py createsuperuser
```
### Run tests ###

```bash
docker exec -it test_web_1 python manage.py test
```

### Iniciar Frontend ###

Dentro del directorio del proyecto, ejecuta el siguiente comando para instalar las dependencias:

```bash
npm install
```

Utilizar el siguiente comando para compilar el proyecto de React:

```bash
npm run build
```
