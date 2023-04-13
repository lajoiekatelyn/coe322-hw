from flask import Flask, request, send_file
import redis
import requests
import json
import os
from matplotlib import pyplot as plt
import numpy as np

app = Flask(__name__)

def get_redis_client(db_num:int, decode:bool):
    
    """
    This function creates a connection to a Redis database
    
    Arguments
        None
    Returns
        redis_database (redis.client.Redis): Redis client
    """

    redis_ip = os.environ.get('REDIS_IP')
    if not redis_ip:
        raise Exception()    

    return redis.Redis(host=redis_ip, port=6379, db=db_num, decode_responses=decode)

rd = get_redis_client(0, True)
rd_img = get_redis_client(1, False)

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def get_route():
    """
    This function either posts, outputs, or deletes all data in the Redis database.

    Arguments
        None
    Returns
        None
    """
    if request.method == 'GET':
        if len(rd.keys())==0:
            return 'There is no data in the database.\n', 400
        output_list = []
        for item in rd.keys():
            output_list.append(json.loads(rd.get(item)))
        return output_list
    elif request.method == 'POST':
        response = requests.get('https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            item = json.dumps(item)            
            rd.set(key, item)
        return f'Data loaded, there are {len(rd.keys())} keys in the db.\n'
    elif request.method == 'DELETE':
        rd.flushdb()
        return f'Data deleted, there are {len(rd.keys())} keys in the db.\n'
    else:
        return 'The method requested does not apply.\n', 400

@app.route('/genes', methods=['GET'])
def get_genes() -> list:
    """
    This function returns all of the keys in the Redis database.

    Arguments
        None
    Returns
        keys (list): unordered list of all keys in the database
    """
    if len(rd.keys())==0:
        return 'There is no data in the database.\n', 400

    return rd.keys()

@app.route('/genes/<string:hgnc_id>', methods=['GET'])
def get_hgnc_id(hgnc_id:str) -> dict:
    """
    This function retrieves a specific gene from the database.

    Arguments
        hgnc_id (str):  HGNC ID of the gene, EX. HGNC:35458
    Returns
        gene_info (dict): all HGNC approved information on the requested gene
    """
    if rd.get(hgnc_id) == None:
        return f'{hgnc_id} is not a gene in the dataset. Please try another.\n', 400

    ret = json.loads(rd.get(hgnc_id))
    return ret

@app.route('/image', methods=['GET', 'POST', 'DELETE'])
def get_image():
    """
    This route creates and deletes images on a Redis database. When there is data in the database, users can send it to themselves using the 'GET' route.

    Arguments:
        None
    Returns:
        image (png): pie chart of where genes are located.
    """
    if request.method == 'GET':
        if rd_img.exists('image'):
            path = './image.png'
            with open(path, 'wb') as f:
                f.write(rd_img.get('image'))
            return send_file(path, mimetype='image/png', as_attachment=True)
        else:
            return 'There are no images in the database.\n', 400
    elif request.method == 'POST':
        if len(rd.keys())==0:
            return 'There is no data in the database; image cannot be created.\n', 400
        locus = {}
        for item in rd.keys():
            item = json.loads(rd.get(item))
            if item['locus_group'] not in locus:
                locus[item['locus_group']]=1
            else:
                locus[item['locus_group']]+=1
        genes = []
        data = []
        for key in locus.keys():
            genes.append(key)
            data.append(locus[key])
        plt.figure()
        plt.pie(data, labels=genes)
        plt.title('Loci of Genes in Dataset')
        plt.savefig('./image.png')
        filebytes = open('./image.png', 'rb').read()
        rd_img.set('image', filebytes)
        return 'Image written to image database.\n'
    elif request.method == 'DELETE':
        rd_img.flushdb()
        return 'Image erased from database.\n'
    else:
        return 'The method requested does not apply.', 400
if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
