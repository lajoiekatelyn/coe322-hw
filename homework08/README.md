# Homework 08: Flask App for HGNC Approved Genes and Symbols Using Redis Database on Kubernetes

## Description
Every gene is unique, and therefore it is important to identify them as so, giving each gene it's own name and symbol. The app and database utilizes public information on HGNC approved genes and their symbols from [genenames.org](https://www.genenames.org/) to ensure that information about each HGNC recognized gene is readily accessible for those who need or are interested in this information.

## gene_api.py
This script contains the application and its queries. It stores and access information concerning HGNC approved genes in the Redis database. In the following subsections, the script requirements (Flask, Redis, and data from the internet) are addressed.

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
As an end user, running the app has four simple steps. First, change the Redis database client host in the `gene_api.py` script from `klajoie-test-redis-service` to `redis-db`. Then, pull the image from the Docker Hub and then build the image. To do so, please run the following command
```
$ docker pull lajoiekatelyn/gene_flask_app:1.0
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

## Kubernetes
To run this app on a Kubernetes cluster, please follow the instructions below.

### Deployment
Each yaml file in this repo, save for `docker-compose.yml`, is a file that needs to be applied to Kubernetes. To do so, enter the following commands in the console from which you have Kubernetes access:
```
$ kubectl apply -f klajoie-test-redis-deployment.yml
$ kubectl apply -f klajoie-test-pvc.yml
$ kubectl apply -f klajoie-test-flask-deployment.yml
$ kubectl apply -f klajoie-test-redis-service.yml
$ kubectl apply -f klajoie-test-flask-service.yml
$ kubectl apply -f klajoie-test-python-debug.yml
```
The console should output confirmation that you properly applied each deployment, persistent volume control, service, etc after each `kube apply -f` command and then you should be good to go using Kubernetes!
NOTE: if users wish to user their own Flask API in the kubernetes cluster, they must change the image being pulled in `klajoie-test-flask-deployment` to their image on Docker Hub and then re-apply the kubernetes depolyment.

### Kubernetes Usage
To use the cluster, first run the following comand
```
$ kubectl get pods
klajoie-test-flask-deployment-57648c5759-t9x5t   1/1     Running   0               102m
klajoie-test-flask-deployment-57648c5759-vjzl7   1/1     Running   0               102m
klajoie-test-redis-deployment-654c66bcb6-smzjm   1/1     Running   0               104m
py-debug-deployment-f484b4b99-r9vff              1/1     Running   0               8h
```

Note the python debug deployment and use it to access the cluster:
```
$ kubectl exec -it py-debug-deployment-f484b4b99-r9vff -- /bin/bash
```

You will end up in a terminal something like:
```
root@py-debug-deployment-f484b4b99-r9vff:/#
```

where you can use any of the commands below, under Usage, replacing `localhost` with `klajoie-test-flask-service`. For example,
```
$ curl klajoie-test-flask-service:5000/data
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

## Usage

| Command | Method | Description |
| --- | --- | --- |
| `/data` | POST | Load HGNC JSON file from the web and store it on the Redis database. |
| | GET | Output the Redis database to the console. |
| | DELETE | Flush all data from the Redis database. |
| `/genes` | GET | Output a list of all genes in the Redis database to the console. |
| `/genes/<hgnc_id>` | GET | Output specific gene from the database to the console. |
| `/image` | GET | Returns image to user in current folder. |
| | POST | Creates image from data in Redis database. |
| | DELETE | Flush created image from Redis database. |

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

### Image Route

#### POST
To create a pie chart of all the gene loci in the HGNC database, provided that there is data loaded into the database:
``` 
$ curl klajoie-test-flask-service:5000/image -X POST
Image written to image database.
```
#### GET
To get the image created from the `POST` command above and transfer it from the Redis database to a user's current directory on their machine,
``` 
$ curl klajoie-test-flask-service:5000/image -output loci_piechart.png
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 22745  100 22745    0     0  3701k      0 --:--:-- --:--:-- --:--:-- 3701k
```
The generated image should look something along the lines of
![Gene loci pie chart.](https://github.com/lajoiekatelyn/coe322-hw/blob/main/homework08/loci_piechart.png)
#### DELETE
To flush the image from the database
``` 
$ curl klajoie-test-flask-service:5000/image -X DELETE
Image erased from database.
```
