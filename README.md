# Backend Super Mami Stock

Proyecto backend para sistema de stock Super Mami (Api)

## Comenzando 馃殌

Instrucciones b谩sicas para correr el proyecto.


### Pre-requisitos 馃搵

Descargar e instalar Python (en su versi贸n 3.9.6). Puede encontrarse en su p谩gina oficial

```
https://www.python.org/downloads/
```
Una vez instalado python, es necesario crear un entorno virtual. Lo hacemos de la siguiente manera:

Abrir una terminal de comandos o CMD y ubicarse en un directorio cualquiera (el que se prefiera para crear el entorno, pero debe ser fuera del directorio de proyecto). Lo hacemos a trav茅s de los comandos cd nombreDirectorio (para ingresar) o cd .. (para salir)


Una vez ubicado en el directorio, ejecutar el siguiente comando reemplazando con el nombre que se le quiera dar al entorno:
```
python3 -m venv nombreEntorno
```

_Se puede observar a trav茅s de el explorador de archivos que lo que gener贸 ese comando no es m谩s que otro directorio con carpetas y archivos_

Ya creado el entorno, lo 煤ltimo necesario es activarlo.

Ejecutamos reemplazando el nombre del entorno que hayamos puesto:

```
cd nombreEntorno/Scripts
```
```
activate
```

_Se tiene que observar que la linea de comando pasa de tener este formato_

C:\Users\usuario\...

a tener este

(nombreEntorno) C:\Users\usuario\...

Significa que el entorno est谩 activo



### Instalaci贸n 馃敡

Procedemos a la instalaci贸n en el entorno virtual las librer铆as y dependencias que tiene el proyecto

En el CMD con el entorno activado, ingresamos al directorio del proyecto hasta donde se encuentre el archivo "requirements.txt" y ejecutamos los siguiente:

```
pip install -r requirements.txt
```

_Esta instalaci贸n se realiza una sola vez_

Una vez terminada la instalaci贸n, ya podemos levantar el proyecto y comenzar a trabajar

Para ello, sobre el directorio que estamos parado en CMD ejecutamos lo siguiente:

```
python manage.py runserver
```

La aplicaci贸n correra en http://localhost:8000/api/


## Autores 鉁掞笍

Creado por Grupo 1 de asignatura Metodolog铆a de Sistemas I, UTN-FRC
