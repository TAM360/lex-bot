import printjson as printjson
from flask import Flask, request, make_response, render_template, jsonify
import json
from pymongo import MongoClient
import random
from bson.objectid import ObjectId
import boto3
from nlp import binary_module, compare

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def mongoInstance():
    client = MongoClient("mongodb://tam:please%5Fdie96@cluster0-shard-00-00-ahzay.gcp.mongodb.net:27017,cluster0-shard-00-01-ahzay.gcp.mongodb.net:27017,cluster0-shard-00-02-ahzay.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true") 
    # MongoClient('localhost', 27017)
    db = client['chatbot_db']
    return db

def addDataToMongo(q, a, db):
    try:
        user = db['queries'] 
        result = user.insert_one({
                'question': q,
                'answer': a
            }).inserted_id
        print(result)
        return result
    
    except Exception as e:
        print(e)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    db = mongoInstance()    
    resp = None
    kwd = request.form['keyword'].lower()
    
    if len(compare(kwd)) > 0: 
        result = binary_module(kwd)
        print (type(result))
        print('result', result[0], type(result))

        result1 = ""
        response = ""
        if(len(result) > 1):
            result1 = result[1]
            response = '{"result" : "' + result[0] +'", "steps" : "' + result1 + '"}'
        else:
            response = '{"result" : "' + result[0] + '"}'

        print('result1', result1, type(result1))
        print('response', response, type(response))
        resp = make_response(response)
        print(addDataToMongo(kwd, result[0], db))

    else:
        lex = boto3.client(
            'lex-runtime', 
            region_name='us-east-1', 
            aws_access_key_id='AKIAJH52Z3SLPZAJ2ELQ', 
            aws_secret_access_key='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'
        )

        response = lex.post_text (
            botName='UniChatBot',
            botAlias='aliasTwo',
            userId='655701873205',
            sessionAttributes={
                'string': 'string'
            },
            requestAttributes={
                'string': 'string'
            },
            inputText= request.form['keyword']
        )
        print('response', type(response), response['message'])
        result = '{"result" : "' + response['message'] + '"}'
        resp = make_response(result)
        print(addDataToMongo(kwd, response['message'], db))
    
    print ('resp', resp)
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)