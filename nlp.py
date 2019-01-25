import nltk
import re, math, json
# nltk.download('punkt')

def compare(query):
    keyword_list = [
        'one', 'two', 'compliment', 
        'convert', 'compliment', 'represent' 
        'number', 'any', 'bits',
        'binary', 'decimal', '+', '-', 
        'sum', 'difference', 'required'
    ]

    tokenize = nltk.word_tokenize(query)
    # print(tokenize)

    return [x for x in tokenize if x in keyword_list] # get common keywords

def check_binary_format(string) : 
    
    p = set(string) 
    s = {'0', '1'} # declare set of '0', '1' . 
  
    # case 1: string has both 1s and 0s
    # case 2: string only has 1s
    # case 3: string only has 0s
    if s == p or p == {'0'} or p == {'1'}: 
        return "yes"
    else: 
        return "no" 

def binary_to_decimal(binary_numbers):
    if len(binary_numbers) == 1:
        steps = ''
        return [int(binary_numbers[0], base = 2), steps]
    
    else: 
        return ['Error! 1 argument required, given 0 or more than 1']


def decimal_to_binary(decimal_numbers):
    if len(decimal_numbers) == 1:
        steps = ''
        return [bin(decimal_numbers[0]).replace("0b", ""), steps]
    
    else: 
        return ["Error! 1 argument required, given 0 or more than 1"]

def one_compliment(x):
    if len(x) == 1:
        temp = ""
        for i in range(0, len(x[0])):
            if x[0][i] == '0':
                temp = temp + '1'
            else: 
                temp = temp + '0'
        print(temp)
        return [temp, "invert every bit of the given bit string"] 

    else:
        return ["Error! 1 argumnent required, given 0."]

# def twos_compliment(binary_numbers):
#     if len(binary_numbers) == 1:
#         compliment = one_compliment(binary_numbers) 
#         return bin(int(compliment, base = 2) + 1).replace('0b', '')
    
#     else:
#         return json.dumps({'error':"Error! 1 argumnent required, given 0."})

def bit_representation(decimal_numbers):
    
    if len(decimal_numbers) == 1:    
        steps = "steps: 1. take log base 2 of the given binary string i.e log(" + str(decimal_numbers[0]) +", base = 2) = " + str(math.log(decimal_numbers[0], 2)) 
        steps = steps + "2. take ceiling of the previous result like this: ceiling(" + str(math.log(decimal_numbers[0], 2)) + ") = " + str(math.ceil(math.log(decimal_numbers[0], 2)))         
        return [math.ceil(math.log(decimal_numbers[0], 2)), steps]
    
    else: 
        return ['Error! 1 arg required, given 0']

def binary_addition(binary_numbers):
    if len(binary_numbers) == 2:
        return [bin(int(binary_numbers[0], 2) + int(binary_numbers[1], 2)).replace("0b", ''), '']
        
    else:
        return ["Error! 2 args required, given 1."]

def binary_subtraction(binary_numbers):
    if len(binary_numbers) == 2:
        return [bin(int(binary_numbers[0], 2) - int(binary_numbers[1], 2)).replace("0b", ''), '']

    else:
        return ["Error! 2 args required, given 1."]

def binary_module(query):
    keyword_list = [
        'one', 'two', 'compliment', 
        'convert', 'compliment', 'represent' 
        'number', 'any', 'bits',
        'binary', 'decimal', '+', '-', 
        'sum', 'difference', 'required'
    ]

    tokenize = nltk.word_tokenize(query)
    # print(tokenize)

    kwd = [x for x in tokenize if x in keyword_list] # get common keywords
    print(kwd) 

    binar_numbers = []
    decimal_numbers = []

    # isolate decimal and binary number arguments. 
    for i in tokenize:
        if re.match(r'[0-9]', i): 
            if check_binary_format(i) == "yes":
                binar_numbers.append(i)
            else:
                decimal_numbers.append(int(i))
            
    # print(binar_numbers, decimal_numbers)

    try:
        if 'one' in kwd and 'compliment' in kwd:
            return one_compliment(binar_numbers)
    
        elif 'required' in kwd and 'bits' in kwd: 
            return bit_representation(decimal_numbers)

        elif 'sum' in kwd or '+' in kwd:
            return binary_addition(binar_numbers)
        
        elif 'difference' in kwd or '-' in kwd:
            return binary_subtraction(binar_numbers)

        elif 'convert' in kwd:
            if "to decimal" in query or "binary to decimal" in query: 
                return binary_to_decimal(binar_numbers)

            elif "to binary" in query or "decimal to binary" in query:
                return decimal_to_binary(decimal_numbers)
        else:
            return ["query format not correct, please repeat the question againg"]

    except:

        raise Exception
        # return ["Sorry, I couldn't understand your question. Please repeat it again."]


# if __name__ == "__main__":
    # print(binary_module("what's the one's compliment of 1010?"))
    # print(binary_module("how many bits are required to represent 37 in binary"))
    # print(binary_module("what's the sum of 10101 and 11"))
    # print(binary_module("11010 - 001"))
    # print(binary_module("convert 10101 to decimal"))
    # print(binary_module("convert 24 from decimal to binary"))
    # print(twos_compliment(['1101011']))