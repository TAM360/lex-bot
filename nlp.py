import nltk
import re, math, json
nltk.download('punkt')

keyword_list = [
    'write', 'one', 'two','ones', 
    'twos', 'binary', 
    "one's", "two's", 'compliment', 
    'convert', 'complement', 'represent' 
    'number', 'bits', 'value', 
    'decimal', '+', '-', 
    'sum', 'difference', 'required'
]

# retrieve common keywords.
def compare(query):
    tokenize = nltk.word_tokenize(query)
    return [x for x in tokenize if x in keyword_list]

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

def binary_to_decimal(binary_numbers, decimal_numbers =None):
    if len(binary_numbers) == 1:
        steps = 'Starting from LSB, take sum of (2*i)^x where i = bit value and x = bit position.<br />'
        steps = steps + ' For this example, <br /><b>' + binary_numbers[0] + ' = '
        sum = 0
        position = len(binary_numbers[0])

        for i in range(0, len(binary_numbers[0]) ):
            sum = sum + (2 * int(binary_numbers[0][i], base = 2) ** position)
            position = position - 1
            steps = steps + '(2*' + binary_numbers[0][i] + ')<sup>' + str(position) + '</sup> + '
        
        steps = steps + ' = ' + str(int(binary_numbers[0], base = 2)) 
        steps = steps + '</b><br />'
        return [str(int(binary_numbers[0], base = 2)), steps[:len(steps) - 3]]
    
    elif len(decimal_numbers) == 1:
        return decimal_to_binary(decimal_numbers)

    else: 
        return ['Error! 1 argument required, given 0 or more than 1', ""]


def decimal_to_binary(decimal_numbers):

    if len(decimal_numbers) == 1:
        steps = 'To convert decimal number into binary, divide the number by 2 repeatedly until<br />'
        steps = steps + 'remainder becomes smaller than 2. Then read all the carry in backward(bottom to top) direction.<br />' 
        steps = steps + ' For this example, <br /> <b>'

        num = decimal_numbers[0]
        count = 0
        carry = 0
        bits = math.ceil(math.log(int(num), 2))
        while (count < bits):
            steps = steps + "Iteration # " + str(count) + ": " + "remainder = " + str(int(num/2))
            carry = num % 2
            num = num / 2
            steps = steps + ', carry = ' + str(int(carry)) + '<br />'
            count = count + 1

        
        steps = steps + "<b/> <br/>"
        return [str(bin(decimal_numbers[0]).replace("0b", "")), steps]
    
    else: 
        return ["Error! 1 argument required, given 0 or more than 1", ""]

def one_compliment(x, y = None):
    if len(x) == 1:
        temp = ""
        for i in range(0, len(x[0])):
            if x[0][i] == '0':
                temp = temp + '1'
            else: 
                temp = temp + '0'
        print(temp)
        return [temp, "invert every bit of the given bit string i.e change 0 to 1 and 1 to 0"] 
    
    elif len(y) == 1:
        temp = bin(int(y[0])).replace("0b", "")
        print(temp)
        temp2 = ""

        for i in range(0, len(temp)):
            if temp[i] == '0':
                temp2 = temp2 + '1'
            else: 
                temp2 = temp2 + '0'
        
        print(temp2)

        result = decimal_to_binary(y)
        steps = "First, convert decimal number into binary number.<br />"\
            "To convert decimal number into binary, "
        
        steps = steps + result[1] 
        steps = steps + "<br /> Then, invert every bit of the given bit string i.e change 0 to 1 and 1 to 0."
        steps = steps + "<br /> Finally, convert the result back to decimal format. For this,"\
            " follow the following steps: <br />"

        steps = steps + binary_to_decimal([temp2])[1]
        return [str(int("0b" + temp2, base = 2)), steps]
    
    else:
        return ["Error! 1 argumnent required, given 0.", ""]

def twos_compliment(binary_numbers, decimal_numbers = None):
    if len(binary_numbers) == 1:
        steps = "apply one's compliment to binary string first and then add 1 to LSB (Least Significant Bit)<br />"
        compliment = one_compliment(binary_numbers) 
        return [str(bin(int(compliment[0], base = 2) + 1).replace('0b', '')), steps + compliment[1]]
    
    elif len(decimal_numbers) == 1:
        temp = [bin(decimal_numbers[0]).replace("0b", "")]
        compliment = one_compliment(temp)
        sum = int("0b" + compliment[0], base = 2) + 1
        
        result = decimal_to_binary(decimal_numbers)
        steps = "First, convert decimal number into binary number.<br />"\
            "To convert decimal number into binary, "
        
        steps = steps + result[1] 
        steps = steps + "<br /> Then, apply one's compliment to binary string and then add 1 to LSB (Least Significant Bit)"
        steps = steps + "<br /> Finally, convert the result back to decimal format. For this,"\
            " follow the following steps: <br />"

        steps = steps + binary_to_decimal([compliment[0]])[1]

        return [str(sum), steps]

    else:
        return ["Error! 1 argumnent required, given 0.", ""]

def bit_representation(decimal_numbers):
    
    if len(decimal_numbers) == 1:    
        steps = "Take log base 2 of the given binary string i.e log<sub>2</sub>(" + str(decimal_numbers[0]) + ") = " + str(math.log(decimal_numbers[0], 2)) 
        steps = steps + "<br />take ceiling of the previous result like this: &lceil;" + str(math.log(decimal_numbers[0], 2)) + "&rceil; = " + str(math.ceil(math.log(decimal_numbers[0], 2)))         
        steps = steps + "<br /> <b>Note: The answer has to be a interference, so we round up to the nearest biggest interger.</b>"
        return [str(math.ceil(math.log(decimal_numbers[0], 2))), steps]
    
    else: 
        return ['Error! 1 arg required, given 0', ""]

def binary_addition(binary_numbers, decimal_numbers = None):
    if len(binary_numbers) == 2:
        return [bin(int(binary_numbers[0], 2) + int(binary_numbers[1], 2)).replace("0b", ''), 
                'Starting from LSB (assumming both arguments to be in base 2), add the bits of each '\
                'argument.<br/ >if the sum is equal to 10 (2 in decimal), then add the carry in next<br />'\
                'bit of 1st argument and place 0 in the final answer.<br />If the sum of bits from both '\
                'arguments is 11 (3 in decimal) then place 1 in the final result and add 1 in the next bit of<br />'\
                'the first argument. Keep repeating these steps untill MSB is reached.<br />']

    elif len(binary_numbers) == 1 and len(decimal_numbers) == 1:
        return [str(int(binary_numbers[0], 2) + decimal_numbers[0]), '<br /> since arguments were in base 2 and base 10, result is generated in base 10']

    elif len(decimal_numbers) == 2:
        return [str(decimal_numbers[0] + decimal_numbers[1]), 
        "Step 1:  Line up the numbers vertically so that the decimal points all lie on a vertical line.<br />"\
        "Step 2: Add extra zeros to the right of the number so that each number has the same number of digits to the right of the decimal place.<br/ />"\
        "Step 3:  Add the numbers as you would whole numbers.  Place the decimal point of the result in line with the other decimal points.<br />"
    ]

    else:
        return ["Error! 2 args required, given 1.", ""]

def binary_subtraction(binary_numbers, decimal_numbers = None):
    if len(binary_numbers) == 2:
        return [str(bin(int(binary_numbers[0], 2) - int(binary_numbers[1], 2)).replace("0b", '')), 
        'Binary subtraction is also similar to that of decimal subtraction with the difference that when<br />'\
        "1 is subtracted from 0, it is necessary to borrow 1 from the next higher order bit<br />"\
        'and that bit is reduced by 1 (or 1 is added to the next bit of subtrahend) and the remainder is 1<br />']

    elif len(binary_numbers) == 1 and len(decimal_numbers) == 1:
        return [str(int(binary_numbers[0], 2) - decimal_numbers[0]), '<br /> since arguments were in base 2 and base 10, result is generated in base 10']
    
    elif len(decimal_numbers) == 2:
        return [str(decimal_numbers[0] -  decimal_numbers[1]), 
        "Step 1: Line up the numbers vertically so that the decimal points all lie on a vertical line.<br />"\
        "Step 2: Add extra zeros to the right of the number so that each number has the same number of digits to the right of the decimal place.<br/ />"\
        "Step 3: Subtract the numbers as you would whole numbers. Place the decimal point of the result in line with the other decimal points.<br />"
    ]

    else:
        return ["Error! 2 args required, given 1.", ""]

def binary_module(query):
    tokenize = nltk.word_tokenize(query)
    print(tokenize)

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
        if (('one' in kwd or 'ones' in kwd or "one's" in kwd) or ('two' not in kwd and 'twos' not in kwd and "two's" not in kwd)) and ('compliment' in kwd or 'complement' in kwd):
            return one_compliment(binar_numbers, decimal_numbers)
    
        elif ('two' in kwd or 'twos' in kwd or "two's" in kwd) and ('compliment' in kwd or 'complement' in kwd):
            return twos_compliment(binar_numbers, decimal_numbers)

        elif 'bits' in kwd: 
            return bit_representation(decimal_numbers)

        elif 'sum' in kwd or '+' in kwd:
            return binary_addition(binar_numbers, decimal_numbers)
        
        elif 'difference' in kwd or '-' in kwd:
            return binary_subtraction(binar_numbers, decimal_numbers)

        elif 'convert' in kwd or 'write' in kwd or 'represent':
            if "to decimal" in query or "binary to decimal" in query or 'decimal' in query: 
                return binary_to_decimal(binar_numbers, decimal_numbers)

            elif "to binary" in query or "decimal to binary" in query or 'binary' in query:
                return decimal_to_binary(decimal_numbers)
        else:
            return ["query format not correct, please repeat the question again.", ""]

    except:
        # raise Exception
        return ["Sorry!, can you repeat your question", ""]


# print(binary_module("what's the one's compliment of 1010?"))
# print(binary_module("how many bits are required to represent 37 in binary"))
# print(binary_module("what's the sum of 10101 and 11"))
# print(binary_module("11010 - 001"))
# print(binary_module("convert 10101 to decimal"))
# print(binary_module("convert 24 from decimal to binary "))
# print(twos_compliment(['1101011']))

# print(binary_module("how do i write 67 in binary"))
# print(binary_module("how do i write 110101 in decimal"))

# print(binary_module("what's the one's compliment of 25"))
# print(binary_module("what's the two's compliment of 24"))

# print(binary_module("26 - 9"))
# print(binary_module("26 + 12"))
