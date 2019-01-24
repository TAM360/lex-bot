import nltk
import re, math
# nltk.download('punkt')

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

def binary_to_decimal(bit_string):
    return int(bit_string, base = 2)

def decimal_to_binary(integer):
    return bin(integer)

def one_compliment(x):
    if len(x) == 1:
        temp = ""
        for i in range(0, len(x[0])):
            if x[0][i] == '0':
                temp = temp + '1'
            else: 
                temp = temp + '0'

        return [temp, "steps: invert every bit of the given binary string i.e change 0 to 1 and 1 to 0."]
    else:
        return "Error! 1 argumnent required, given 0."

def bit_representation(decimal_numbers):
    steps = "steps: 1. take log base 2 of the given binary string i.e log(" + str(decimal_numbers[0]) +", base = 2) = " + str(math.log(decimal_numbers[0], 2)) 
    steps = steps + "2. take ceiling of the previous result like this: ceiling(" + str(math.log(decimal_numbers[0], 2)) + ") = " + str(math.ceil(math.log(decimal_numbers[0], 2))) 
    return [math.ceil(math.log(decimal_numbers[0], 2)), steps]

def binary_addition(binary_numbers):
    if len(binary_numbers) == 2:
        return bin(int(binary_numbers[0], 2) + int(binary_numbers[1], 2)).replace("0b", "")
    else:
        return "Error! 2 args required, given 1."

def binary_subtraction(binary_numbers):
    if len(binary_numbers) == 2:
        return bin(int(binary_numbers[0], 2) - int(binary_numbers[1], 2)).replace("0b", "")
    else:
        return "Error! 2 args required, given 1."

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
    
    # KEYWORDS           | QUESTION
    # -------------------|---------------------------------------------------
    # one, compliment    | what's the one's compliment of x
    # base, one, two,    | convert x into base 2 number
    # convert            |                             
    # two, compliment    | what's the two's compliment of x
    # bits, represent    | no. of bits required to represent
    # convert, decimal,  | convert x from binary to decimal/decimal to binary
    # binary             | 
    # required, bits     | how many bits are required to represent 37 in binary
    # represent          |

    kwd = [x for x in tokenize if x in keyword_list] # get common keywords
    print(kwd) 

    # isolate decimal and binary number arguments. 
    binar_numbers = []
    decimal_numbers = []
    for i in tokenize:
        if re.match(r'[0-9]', i): 
            if check_binary_format(i) == "yes":
                binar_numbers.append(i)
            else:
                decimal_numbers.append(int(i))
            
    print(binar_numbers, decimal_numbers)

    if 'one' in kwd and 'compliment' in kwd: # for 1's compliment
        return one_compliment(binar_numbers)
    try:
        if 'required' in kwd and 'bits' in kwd: # number of bits for decimal number representation
            return bit_representation(decimal_numbers)

        elif 'sum' in kwd or '+' in kwd:
            return binary_addition(binar_numbers)
        
        elif 'difference' or '-':
            return binary_subtraction(binar_numbers)
    except Exception:
        print(Exception)
        return "Sorry, I couldn't understand your question. Please repeat it again."


if __name__ == "__main__":
    print(binary_module("what's the one's compliment of 1010?"))
    # print(binary_module("how many bits are required to represent 37 in binary"))
    # print(binary_module("what's the sum of 10101 and 11"))
    # print(binary_module("11010 - 001"))
    # print(binary_module("convert 10101 to decimal"))
    # print(one_compliment('10101'))
    # print(binary_module("convert 24 from decimal to binary"))
    
    
        

