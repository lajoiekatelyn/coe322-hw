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

#### docker-compose for Developers

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
