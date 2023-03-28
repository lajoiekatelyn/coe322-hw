# Homework 06: Flask App for HGNC Approved Genes and Symbols Using Redis Database

## Description
Every gene is unique, and therefore it is important to identify them as so, giving each gene it's own name and symbol. The app and database utilizes public information on HGNC approved genes and their symbols from [genenames.org](https://www.genenames.org/) to ensure that information about each HGNC recognized gene is readily accessible for those who need or are interested in this information.

## gene_api.py
This script contains the applicaiton and its queries. It stores and access information concerning HGNC approved genes in the Redis database. In the following subsections, the script requirements (Flask, Redis, and data from the internet) are addressed.

### Flask
This program uses the Python Flask library. Flask is a web framework used to develop generalized web applications. To install Flask, please enter the following command into your terminal:

```
$ pip3 install --user flask
```

### Redis
This script uses the Redis, a NoSQL database, to store all app data to ensure that it is not lost when the Flask app stops running and allow for multiple processes to access the data at once. If the Redis Python library is not already installed on your machine and you plan on doing development with this repo, please install it using
```
pip3 install redis
```
otherwise, Docker will take care of the Redis image for this application.

### Required Data
Data required for this app is the [Current JSON format hgnc_complete set file](https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json) from [genenames.org](https://www.genenames.org/).  , which is accessed using the Python `requests` library. If requests is not installed on your machine, please install it using the following command in your terminal:

```
$ pip3 install --user requests
```
The data can also be accessed in text format (`.txt`). Both file formats contain headers and responses. The important information for this app is the response key, which is in the form of a list of dictionaries containing HGNC approved information on genes.

## Docker
To ensure functionality across macnines, this app is containerized according to the included DockerFile and launched according to the included docker-copose.yml file. To run the app as an end user, please refer to the Pull the Docker Image and docker-compose sections below. To develop using the app in this repo, please refer to the DockerFile section below.

### Pull and Build the Docker Image
As an end user, running the app has three simple steps. The first two are to pull the image from the Docker Hub and then build the image. To do so, please run the following command
```
$ docker pull lajoiekatelyn/gene_flask_app:1.0 [DOUBLE CHECK THIS]
```
and then, in the root of the repo,
```
$ docker build -t lajoiekately/gene_flask_app:1.0 .
```
Then the image should be good to go.

### docker-compose
To launch the app alongside Redis, please run the following command in the root of the directory
```
$ docker-compose up -d
```
to run the app and Redis in the background. Then, to terminate the app and Redis,
```
$ docker-compose down
```

### DockerFile
To build upon this repo, any new package used in the main script will need to be added to the DockerFile. Then, the docker image will need to be rebuilt. To do so,
```
$ docker build -t <docker_username>:gene_flask_app:<version_number>
```
where `<docker_username>` is your Docker username and `<version_number>` is the verion of the image that you wish to build.

#### docker-compose for Developers
If you develop and push a new Docker image to Docker Hub, you will need to change the name of the Docker image in docker-compose.yml to the name of the image that you pushed.

NOTE: for the purpose of using docker-compose, the host declared for the Redis client in the get_redis_client() funciton in gene_api.py is set to `redis-db`. In order to develop using Flask, change the host to `127.0.0.1`. Then, when it comes time to use docker-compose again, change it back to `redis-db`.

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
```
$ curl localhost:5000/data
[
  {
    "_version_": 1761544709796265984,
    "agr": "HGNC:41931",
    "date_approved_reserved": "2011-05-19",
    "date_modified": "2019-02-14",
    "date_name_changed": "2019-02-14",
    "ensembl_gene_id": "ENSG00000250359",
    "entrez_id": "100129564",
    "hgnc_id": "HGNC:41931",
    "location": "5q14.3",
    "location_sortable": "05q14.3",
    "locus_group": "pseudogene",
    "locus_type": "pseudogene",
    "name": "PTP4A1 pseudogene 4",
    "prev_name": [
      "protein tyrosine phosphatase type IVA, member 1 pseudogene 4"
    ],
    "pseudogene.org": "PGOHUM00000235686",
    "refseq_accession": [
      "NG_029015"
    ],
    "status": "Approved",
    "symbol": "PTP4A1P4",
    "uuid": "c8ea2431-d082-4180-8240-c21f8ed78ee5",
    "vega_id": "OTTHUMG00000162586"
  }, 
  ...
]
```

#### DELETE
```
$ curl localhost:5000/data -X DELETE
Data deleted, there are 0 keys in the db.
```

### Genes Route
The `/genes` route outputs a list of all the HGNC genes loaded into the Redis database. Each gene output corresponts to a key in the database hash.
```
$ curl localhost:5000/genes
[
  "HGNC:47340",
  "HGNC:52615",
  "HGNC:40425",
  "HGNC:25072",
  "HGNC:7115",
  "HGNC:46408",
  "HGNC:4413",
  "HGNC:15519",
  "HGNC:51874",
  "HGNC:42050",
  "HGNC:12738",
  "HGNC:39491",
  "HGNC:31541",
  "HGNC:28286",
  "HGNC:9987",
  "HGNC:46681",
  "HGNC:52504",
  "HGNC:37246",
  "HGNC:35886",
  "HGNC:31548",
  ...
]
```

### Genes HGNC ID Route
The `/genes<hgnc_id>` route provides all information stored in the Redis key corresponding to the <hgnc_id> input in the curl query.
```
$ curl localhost:5000/HGNC:41931
{
  "_version_": 1761544709796265984,
  "agr": "HGNC:41931",
  "date_approved_reserved": "2011-05-19",
  "date_modified": "2019-02-14",
  "date_name_changed": "2019-02-14",
  "ensembl_gene_id": "ENSG00000250359",
  "entrez_id": "100129564",
  "hgnc_id": "HGNC:41931",
  "location": "5q14.3",
  "location_sortable": "05q14.3",
  "locus_group": "pseudogene",
  "locus_type": "pseudogene",
  "name": "PTP4A1 pseudogene 4",
  "prev_name": [
    "protein tyrosine phosphatase type IVA, member 1 pseudogene 4"
  ],
  "pseudogene.org": "PGOHUM00000235686",
  "refseq_accession": [
    "NG_029015"
  ],
  "status": "Approved",
  "symbol": "PTP4A1P4",
  "uuid": "c8ea2431-d082-4180-8240-c21f8ed78ee5",
  "vega_id": "OTTHUMG00000162586"
}
```
