import boto3
import requests, json

#------------------------ for lex bot 'TestBot' ----------------------#
# lex = boto3.client('lex-runtime')

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

# print(response['message'])

# -------------------- for lex bot 'UniChatBot' -----------------------#

lex = boto3.client(
    'lex-runtime', 
    region_name='us-east-1', 
    aws_access_key_id='AKIAJH52Z3SLPZAJ2ELQ', 
    aws_secret_access_key='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'
)

response = lex.post_text(
    botName='UniChatBot',
    botAlias='aliasTwo',
    userId='655701873205',
    sessionAttributes={
        'string': 'string'
    },
    requestAttributes={
        'string': 'string'
    },
    inputText='do you know'
) 
print(response)