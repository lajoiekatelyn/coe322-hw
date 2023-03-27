# Homework 06: Flask App for HGNC Approved Genes and Symbols Using Redis Database

## Description

## gene_api.py

#### Flask

#### Redis

#### Required Data

## Docker

### Pull the Docker Image

### docker-compose

### DockerFile

## Usage

| Command | Method | Description |
| --- | --- | --- |
| `/data` | POST | Load HGNC JSON file from the web and store it on the Redis database. |
| | GET | Output the Redis database to the console. |
| | DELETE | Flush all data from the Redis database. |
| `/genes` | GET | Output a list of all genes in the Redis database to the console. |
| `/genes/<hgnc_id>` | GET | Output specific gene from the database to the console. |

## Example Output

### Data Route
The `/data` route functions according to three different methods: POST, GET, and DELETE. If no specific method is called using `-X <METHOD>` at the end of the curl query, it will default to GET.

#### POST
```
$ curl localhost:5000/data -X POST
Data loaded, there are 43625 keys in the db.
```

#### GET
`$ curl localhost:5000/data`

#### DELETE
```
$ curl localhost:5000/data -X DELETE
Data deleted, there are 0 keys in the db.
```

### Genes Route
The `/genes` route outputs a list of all the HGNC genes loaded into the Redis database. Each gene output corresponts to a key in the database hash.
```
$ curl localhost:5000/genes
[SOME OUTPUT]
```

### Genes HGNC ID Route
The `/genes<hgnc_id>` route provides all information stored in the Redis key corresponding to the <hgnc_id> input in the curl query.
```
$ curl localhost:5000/<hgnc_id>
[SOME OUTPUT]
```
