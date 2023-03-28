from flask import Flask, request
import redis
import requests
import json

app = Flask(__name__)

def get_redis_client():
    return redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

rd = get_redis_client()

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def get_route():
    """
    """
    if request.method == 'GET':
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
        return 'The method you requested does not apply.\n', 400

@app.route('/genes', methods=['GET'])
def get_genes() -> list:
    return rd.keys()

@app.route('/genes/<string:hgnc_id>', methods=['GET'])
def get_hgnc_id(hgnc_id:str) -> dict:
    """
    
    """
    if rd.get(hgnc_id) == None:
        return f'{hgnc_id} is not a gene in the dataset. Please try another.\n', 400

    ret = json.loads(rd.get(hgnc_id))
    return ret

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
