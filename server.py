import printjson as printjson
from flask import Flask, request, make_response, render_template, jsonify
import json
from pymongo import MongoClient
import random
from bson.objectid import ObjectId
import boto3
from nlp import binary_module, compare
import re

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

        result1 = ""
        response = ""
        if(len(result) > 1):
            result1 = result[1]
            response = '{"result" : "' + result[0] + '", "steps": "<br /><b>STEPS:</b> <br/>' + result1 + '"}'
        else:
            response = '{"result" : "' + result[0] + '"}'

        resp = make_response(response)
        print(addDataToMongo(kwd, result[0], db))

    elif kwd == 'help':
        guide = "Hi! My name is <b><i>Serina</i></b>. I will be your guide. I will assist you in academics. I has 2 modules:<br/>"\
                "<b>University Module</b> and <b>Binary Module</b><br>"\
                "University Module: This module can answer questions about"\
                "program details, available courses etc <br/>"\
                "Binary Module: Submit any mathematical queries related with "\
                "binary numbers and it will provide step by step solution. It "\
                "can solve 1's compliment, 2's compliment, base converion "\
                "(binary to decimal/decimal to binary), addition and subtraction."\
                "It can also perform signed binary calculation where we are using the two’s compliment of the number to represent its negative number. User can also"\
                "specify the number of bits in which the answer is required. If the user specified bits are less than minimum bits required for answer, the answer will be shown in minimum required bits."\
                "Following are the sample questions. You can follow any of these formats to get the results<br/> "\
                "1. what's the one's compliment of 1010?<br/>"\
                "2. what's the one's compliment of 1010 in base10?<br/>"\
                "3. what's the two's compliment of -1010?<br/>"\
                "4. what's the two's compliment of -1010 in base ten?<br/>"\
                "5. what's the one's compliment of 12 in 13bit?<br/>"\
                "6. what's the one's compliment of -12?<br/>"\
                "7. how many bits are required to represent 37 in binary?<br/>"\
                "8. how many bits are required to represent -37 in binary?<br/>"\
                "9. what's the sum of 10101 and 11?<br/>"\
                "10. what will be the answer for 11010 - 001?<br/>"\
                "11. what will be the answer for -2 + 5 in 10bit?<br/>"\
                "12. what will be the answer for 2 - 5?<br/>"\
                "13. what will be the answer for 2 - -5?<br/>"\
                "14. what will be the answer for -2 - -5?<br/>"\
                "15. convert 10101 to decimal<br/>"\
                "16. convert 24 from decimal to binary<br/>"\
                "17. convert 110 from decimal to binary in base10 (or else it will give error for converting a binary number to binary again)<br/>"\
                "18. how many bits are required to represent 111 in binary in base10?<br/><br/>"\
                "Note:<br/>"\
                "Spaces are required between operator and operands. If the space is not provided, it will be considered as a magnitude of the respective operand.<br/>"\
                "For example ( 100 - 10 ), (100 + 10), (100 - -10), (-100 + -10)<br/>"\
                "By Default, it takes numbers as binary if it only consists on 1’s and 0’s, e.g. 1, 11, 101.<br/>"\
                "If you want them to be considered decimal, add keyword ‘base10’ or ‘base ten’ along, e.g. '24 - 10 in base10'<br/>"\
                "Don’t use 1’s, 1s, 2’s and 2s as keywords for one’s and two’s complement."
        result = '{"result" : "' + guide + '"}'
        resp = make_response(result)

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
        
        lexResponse = response['message'].replace('"', "")
       
        print('response', type(response), response.__str__())
        #if '|' in lexResponse or 'noun' in lexResponse or 'verb' in lexResponse:
        #    result = '{"result" : ' + lexResponse + '}'
        #else:
        lexResponse = lexResponse.replace("\\n", "<br/>")
        result = '{"result" : "' + lexResponse + '"}'
        print ("result " + result)
        resp = make_response(result)
        print(addDataToMongo(kwd, lexResponse, db))
    
    print ('resp', resp)
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)