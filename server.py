import printjson as printjson
from flask import Flask, request, make_response, render_template
import json
from pymongo import MongoClient
import random
from bson.objectid import ObjectId
import boto3

app = Flask(__name__)
questions = ["Which subject are you interested it?","Do you like fishing?","Do you have a pet?", "What are your hobbies?"]

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def mongoInstance():
    client = MongoClient("mongodb+srv://tam2:please%5Fdie98@cluster0-ahzay.gcp.mongodb.net/test?retryWrites=true") 
    # MongoClient('localhost', 27017)
    db = client['new_db']
    return db

def addUser(name, db):
    try:
        user = db['users'] # get 'users' collection
        result = user.insert_one({
                'name':name,
                'queries': []
            }).inserted_id
        print(result)
        return result

    except Exception as e:
        print(e)

def addUserQuestion(db, user_id, question, category = ''):
    """ user_id has the format ObjectId(<alpha-numerica-string>) """
    try:
        queary = db['questions']
        result = queary.insert_one({
            'question': question,
            'category': category
        }).inserted_id

        db['users'].update_one(
            {
                '_id': user_id
            },
            {
                '$addToSet': {'queries': {'question': result, 'answer': ''}}
            }
        )
        return result
    except Exception as e:
        print(e)

def addUserAnswer(db, user_id, question_id, answer, category=''):
    """ user_id & question_id has the format ObjectId(<alpha-numerica-string>) """
    try:
        solution = db['answers'] # get answers collections
        result = solution.insert_one(
            {
                'answer': answer,
                'category': ''
            }
        ).inserted_id

        db['users'].update_one(
            { # filter parameters
                '_id': user_id,
                'queries.question': question_id
            },
            { # update parameters
                '$set': {
                    'queries.$.answer': result
                }
            }
        )
    except Exception as e:
        print(e)

def getAnswer(data, userID): #here we will implement our logic for giving an intelligent. For now, it is for temporary questions

    outputstr = ""
    if(("Yes" in data) or ("yes" in data) or ("sure" in data) or ("Sure" in data)):
        if(userID == '-1') :
            user_id = addUser('new user', db)
            userID = JSONEncoder().encode(user_id)
        outputstr = "Okay! Please, tell me your name first."

    else:
        if(userID != "-1"):
            user = db.users.find_one({'_id': ObjectId(userID.strip('\"'))})
            print(user["name"])
            if (user) and (user["name"] == "new user"):
                outputstr = data + ", Have a good day!"
                newvalues = {"$set": {"name" : data}}
                db.users.update_one({"_id" : ObjectId(userID.strip('\"'))}, newvalues)
                for x in db.users.find():
                    print(x)
            else:
                temp = (random.random()*10)%4
                outputstr = questions[int(temp)]
        else:
            temp = random.random() % 4
            outputstr = questions[int(temp)]
    user = db.users.find_one({'_id': ObjectId(userID.strip('\"'))})
    ifQuestionExist = db.questions.find_one({'question': outputstr})
    questionid= ""
    if (ifQuestionExist or outputstr.find(data) == -1):
        questionid=addUserQuestion(db,  ObjectId(userID.strip('\"')), outputstr)
    if(questionid != ""):
        addUserAnswer(db,  ObjectId(userID.strip('\"')), questionid, data)
    x = {
        "result": outputstr,
        "userid": userID
    }
    print("result " + outputstr)
    print("userid " + userID.__str__())

    return json.dumps(x)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # lex = boto3.client(
    #     'lex-runtime', 
    #     region_name='us-east-1', 
    #     aws_access_key_id='AKIAIWW7FBGUJ5ZZHDYQ', 
    #     aws_secret_access_key='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'
    # )

    # response = lex.post_text(
    #     botName='TestBot',
    #     botAlias='aliasOne',
    #     userId='655701873205',
    #     sessionAttributes={
    #         'string': 'string'
    #     },
    #     requestAttributes={
    #         'string': 'string'
    #     },
    #     inputText='hi'
    # ) 
    # return response['message']
    # # print(response['message'])
    data = request.form['keyword']
    userID = request.form['userId']

    result = getAnswer(data, userID)
    print (result )
    resp = make_response(json.dumps(result))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    db = mongoInstance()
    app.run(host='127.0.0.1', debug=True)