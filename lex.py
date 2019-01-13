import boto3
import requests, json

lex = boto3.client('lex-runtime')

response = lex.post_text(
    botName='TestBot',
    botAlias='aliasOne',
    userId='655701873205',
    sessionAttributes={
        'string': 'string'
    },
    requestAttributes={
        'string': 'string'
    },
    inputText='hi'
) 

print(response)
