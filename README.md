# Desafio Cargofive
### Instalación 🔧

Situarse en el proyecto y ejecutar los siguientes pasos:

Instalar docker e iniciar el compose
```
docker-compose up --build
```
Ejecutar migraciones

```
docker-compose run web python manage.py migrate 
```

Ingresar al aplicativo
```
http://127.0.0.1:8000/
```