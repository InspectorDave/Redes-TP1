# TP1 Redes

Este es el repositorio para el desarrollo del TP1 de la materia Redes (TA048) de la Facultad de Ingeniería de la Universidad de Buenos Aires.

# Objetivo

En este trabajo práctico se busca implementar un protocolo stop and wait y un protocolo GoBackN sobre el protocolo de transporte UDP. Para lo cual se implementará una estructura cliente-servidor, en la que el servidor pueda mantener varias conexiones activas simultáneas.

# Integrantes

| <center>Alumno</center> | <center>Padrón</center> | <center>Mail</center> |
|:------------------------|:-----------------------:|:----------------------|
| **Mundani Vegega, Ezequiel** | 102312 | emundani@fi.uba.ar | 
| **Sicca, Fabio** | 104892 | fsicca@fi.uba.ar | 

# Cómo correr el proyecto

El proyecto está hecho en python 3.10, consiste de tres programas independientes.

## Para correr el server

```
python3 start-server.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
```
```
optional arguments:
-h, --help show this help message and exit
-v, --verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host service IP address
-p, --port service port
-s, --storage storage dir path
```

## Para correr el upload

```
python3 upload.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s FILEPATH] [-n FILENAME] [-r PROTOCOL]
```
```
optional arguments:
-h, --help show this help message and exit
-v, --verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host server IP address
-p, --port server port
-s, --src source file path
-n, --name file name
-r,  pRotocol type, can be 's' or 'g'
```

## Para correr el download

```
python3 download.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME] [-r PROTOCOL]
```
```
optional arguments:
-h, --help show this help message and exit
-v, --verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host server IP address
-p, --port server port
-d, --dst destination file path
-n, --name file name
-r,  pRotocol type, can be 's' or 'g'
```