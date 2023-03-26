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
            output_list.append(rd.hgetall(item))
        return output_list
    elif request.method == 'POST':
        response = requests.get('https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        # with open('hgnc_complete_set.json', 'r') as f:
            # response = json.load(f)
        for item in response.json()['response']['docs']:
        # for item in response['response']['docs']:
            key = f'{item["hgnc_id"]}'
            for sub_item in item:
                if type(item[sub_item]) == list:
                    temp = ''
                    for element in item[sub_item]:
                        temp += str(element) + '|'
                    item[sub_item] = temp[:-1]
            # print(key, '\n', type(item))
            rd.hset(key, mapping=item)
        return f'Data loaded, there are {len(rd.keys())} keys in the db.\n'
    elif request.method == 'DELETE':
        redis.flushdb()
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
    return rd.hgetall(hgnc_id)    

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
