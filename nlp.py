import nltk
import re, math
# nltk.download('punkt')

def check_binary_format(string) : 
  
    # set function convert string 
    # into set of characters . 
    p = set(string) 
  
    # declare set of '0', '1' . 
    s = {'0', '1'} 
  
    # check set p is same as set s 
    # or set p contains only '0' 
    # or set p contains only '1' 
    # or not, if any one conditon 
    # is true then string is accepted 
    # otherwise not . 
    if s == p or p == {'0'} or p == {'1'}: 
        return "yes"
    else: 
        return "no" 

def one_compliment(x):
    original = int(x[0], 2)
    compliment = bin(~int(x[0], 2)) 
    # print(original)
    return bin(int(compliment, 2)).replace("0b", "")

def binary_module(query):
    keyword_list = [
        'one', 'two', 'compliment', 
        'convert', 'compliment', 'represent' 
        'number', 'any', 'bits',
        'binary', 'decimal', '+', '-', 
        'sum', 'difference'
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
    # print(kwd) 

    # extract arguments assuming that they're given in binary format
    x = []
    y = []
    for i in tokenize:
        if re.match(r'[0-1]', i): 
            if check_binary_format(i) == "yes":
                x.append(i)
            else:
                y.append(i)
            
    print(x, y)

    if 'one' in kwd and 'compliment' in kwd: # for 1's compliment
        return one_compliment(x)
    elif 'required' in kwd and 'bits' in kwd:
        return math.ceil(math.log(x[0], base = 2))
    
if __name__ == "__main__":
    print(binary_module("what's the one's compliment of 1010?"))
    # print(binary_module("how many bits are required to represent 37 in binary"))
    # print(binary_module("what's the sum of 10101 and 11"))
    # print(binary_module("convert 10101 to decimal"))
    # print(one_compliment('10101'))
    # print(binary_module("convert 24 from decimal to binary"))
    
    
        

