import nltk
import re, math, json
nltk.download('punkt')
required_bits= 4
default_bits = 0
isSignednumber = False
userbits = 0
keyword_list = [
    'write', 'one', 'two','ones',
    'twos', 'binary', 
    "one's", "two's", 'compliment', 
    'convert', 'complement', 'represent',
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
            steps = steps + '(2*' + binary_numbers[0][i] + ')^' + str(position) + ' + '
        
        steps = steps[0: len(steps) - 2]
        steps = steps + ' = ' + str(int(binary_numbers[0], base = 2)) 
        steps = steps + '</b><br/>'
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
        if(num > 0):
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
        else: 
            steps = "<b> its a signed number.</b>"
        answer = str(bin(decimal_numbers[0]).replace("0b", ""))
        answer.zfill(required_bits)
        return [answer, steps]
    
    else: 
        return ["Error! 1 argument required, given 0 or more than 1", ""]

def one_compliment(x, y = None):
    if len(x) == 1:
        a = x[0]
        a = a.zfill(required_bits)
        temp = ""
        for i in range(0, len(a)):
            if a[i] == '0':
                temp = temp + '1'
            else: 
                temp = temp + '0'
        print(temp)
        result = "invert every bit of the given bit string i.e change 0 to 1 and 1 to 0 : <br />" + a + " ==> " +  temp
        print(result)

        return [temp,result] 
    
    elif len(y) == 1:
        temp = bin(int(y[0])).replace("0b", "")
        temp = temp.zfill(required_bits)
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
        return ["Base 2: ( " + temp2 + " ) , Base 10: ( " + str(int("0b" + temp2, base = 2)) + ')', steps]
    
    else:
        return ["Error! 1 argumnent required, given 0.", ""]

def twos_compliment(binary_numbers, decimal_numbers = None):
    if len(binary_numbers) == 1:
        steps = "apply one's compliment to binary string first and then add 1 to LSB (Least Significant Bit)<br />"
        compliment = one_compliment(binary_numbers)
        bitlen = compliment[0].__len__()
        answer = str(bin(int(compliment[0], base = 2) + 1).replace('0b', ''))
        answer = answer.zfill(bitlen)
        answer = answer.zfill(required_bits)
        return [answer , steps + compliment[1]]
    
    elif len(decimal_numbers) == 1:
        temp = [bin(decimal_numbers[0]).replace("0b", "")]
        compliment = one_compliment(temp)
        sum = int("0b" + compliment[0], base = 2) + 1
       
        result = decimal_to_binary([sum])

        steps = "First, convert decimal number into binary number.<br />"\
            "To convert decimal number into binary, "

        steps = steps + result[1] 
        steps = steps + "<br /> Then, apply one's compliment to binary string and then add 1 to LSB (Least Significant Bit)"
        steps = steps + "<br /> Finally, convert the result back to decimal format. For this,"\
            " follow the following steps: <br />"
        steps = steps + binary_to_decimal([result[0]])[1]
        result[0] = result[0].zfill(required_bits)
        dec_answer = "Base 2 ( " + result[0] + " ) , Base 10 ( " +str(sum) + ' )'
        return [dec_answer, steps]

    else:
        return ["Error! 1 argumnent required, given 0.", ""]

def bit_representation(decimal_numbers):

    if len(decimal_numbers) == 1:    
        steps = "Take log base 2 of the given binary string i.e log<sub>2</sub>(" + str(decimal_numbers[0]) + ") = " + str(math.log(decimal_numbers[0], 2)) 
        steps = steps + "<br />take ceiling of the previous result like this: &lceil;" + str(math.log(decimal_numbers[0], 2)) + "&rceil; = " + str(math.ceil(math.log(decimal_numbers[0], 2)))         
        steps = steps + "<br /> <b>Note: The answer has to be a integer, so we round up to the nearest biggest integer.</b>"
        answer = str(math.ceil(math.log(decimal_numbers[0], 2)))
        return [answer, steps]
    
    else: 
        return ['Error! 1 arg required, given 0', ""]

def getBinTwosComplement(num, reqBit):
    steps = "apply one's compliment to binary string first and then add 1 to LSB (Least Significant Bit)<br />"
    print("num before: ", num)
    num = num.zfill(reqBit)
    if(userbits > num.__len__()+1):
        num = num.zfill(userbits)
    else:
        num = num.zfill(num.__len__()+1)
    print("num after: ", num)
    a = num
    print("a " , a)
    temp = ""
    for i in range(0, len(a)):
        if a[i] == '0':
            temp = temp + '1'
        else: 
            temp = temp + '0'
    print("temp " , temp)
    print("compliment: ", temp)
    bitlen = temp.__len__()
    answer = str(bin(int(temp, base = 2) + 1).replace('0b', ''))
    print("answer: ", answer[0])
    answer = answer.zfill(bitlen)
    answer = answer.zfill(required_bits)
    return [answer , steps ,"bin"]

def getIntTwosComplement(num, reqBit):
    print("getIntTwosComplement")
    global userbits
    print("num " , num)
    print("reqBit " , reqBit)
    temp = bin(num).replace("0b", "")
    temp=temp.zfill(reqBit)
    print("temp " , temp)
    print("temp len " , len(temp))
    print("temp type " , type(temp))
    a = temp
    print("a " , a)
    print("len(a) " , len(a))
    temp = ""
    for i in range(0, len(a)):
        if a[i] == '0':
            temp = temp + '1'
        else: 
            temp = temp + '0'
    print("temp " , temp)
    sum = int("0b" + temp, base = 2) + 1
    print("sum ", sum)
    result = decimal_to_binary([sum])
    print("result ", result)
    binary_res = result[0]
    print("userbits " , userbits)
    print("binary_res before: ", binary_res)
    if(userbits > binary_res.__len__()+1):
        binary_res = binary_res.zfill(userbits)
    print("binary_res before: ", binary_res)    
    steps = "First, convert decimal number into binary number.<br />"\
        "To convert decimal number into binary, "
    steps = steps + result[1] 
    steps = steps + "<br /> Then, apply one's compliment to binary string and then add 1 to LSB (Least Significant Bit) to get its negative representation i.e. " + binary_res
    steps = steps + binary_to_decimal([binary_res])[1]
    return [binary_res, steps,"int", str(sum)]


def getDecimal(num,isSigned):
    print("num " ,  num)
    numLen = num.__len__()
    print("numLen " ,  numLen)
    decimal_rep=""
    if(isSigned):
        if(num[0] == "0"):
            print("decimal_rep " ,  str(int(num, base = 2)))
            decimal_rep = str(int(num, base = 2))
        else:
            num1 = ""
            num1 = num1.zfill(numLen) 
            print("num1 " ,  num1)
            num1 = '1' + num1[1:]
            print("num1 " ,  num1)
            dec1 = int(num1, base = 2) * -1
            print("dec1 " ,  dec1)
            num = '0' + num[1:]
            print("num " ,  num)
            dec = int(num, base = 2)
            print("dec " ,  dec)
            decimal_rep = str(dec1 + dec)
    else:
        print("decimal_rep " ,  str(int(num, base = 2)))
        decimal_rep = str(int(num, base = 2))
    print("decimal_rep " ,  decimal_rep)

    return decimal_rep


def binary_add_sub(op_type,all_numbers,binary_numbers,decimal_numbers = None):
    isDoubleNeg = False
    global isSignednumber
    if(all_numbers[1][2]=="-"):
        isSignednumber = True
    result = []
    print("op_type ", op_type)
    print("all_numbers[1][2] ", all_numbers[1][2])
    if(op_type == "subtraction"):
        if(all_numbers.__len__() > 1):
            if(all_numbers[1][2]=="-"):
                isDoubleNeg = True
                op_type = "addition"
                all_numbers[1][2] = "+"
            else:
                op_type = "addition"
                all_numbers[1][2] = "-"
    if(all_numbers[1][2]=="-" or all_numbers[0][2]=="-"):
        isSignednumber = True
    print(all_numbers)
    binaries=[]
    for i in all_numbers:
        if(i[2] == "-"):
            if(i[1] == "int"):
                bin_rep = decimal_to_binary([i[0]])
                i.append(bin_rep[0].__len__()+1)
                binaries.append(bin_rep[0])
            else:
                i.append(i[0].__len__()+1)
                binaries.append(i[0])
        else:
            if(i[1] == "int"):
                bin_rep = decimal_to_binary([i[0]])
                i.append(bin_rep[0].__len__())
                binaries.append(bin_rep[0])
            else:
                i.append(i[0].__len__())
                binaries.append(i[0])
    if(all_numbers[0][3] < all_numbers[1][3]):
        all_numbers[0][3] = all_numbers[1][3]
    else:
        all_numbers[1][3] = all_numbers[0][3]
    print(all_numbers)
    for i in all_numbers:
        if(i[2] == "-"):
            if(i[1] == "int"):
                print("- int  getIntTwosComplement")
                result.append(getIntTwosComplement(i[0],i[3]))
            else:
                print("- bin  getBinTwosComplement")
                result.append(getBinTwosComplement(i[0],i[3]))
        else:
            if(i[1] == "int"):
                print("+ int  no complement")
                bin_rep = decimal_to_binary([i[0]])
                print("bin_rep ", bin_rep)
                bin_rep[0] = bin_rep[0].zfill(i[3])
                print("bin_rep[0] ", bin_rep[0])
                result.append([bin_rep[0], bin_rep[1],"int", str(i[1])])
            else:
                i[0] = i[0].zfill(i[3])
                print("+ bin  no complement")
                result.append([i[0] , "" ,"bin"])
    print("result ",result)
    op0 = result[0][0]
    op1 = result[1][0]
    print("op0 " , op0)
    print("op1 " , op1)
    op0len = op0.__len__() 
    op1len = op1.__len__()
    if(op0len > op1len):
        op1 = op1.zfill(op0len)
    else:
        op0 = op0.zfill(op1len)
    print("op0 " , op0)
    print("op1 " , op1)
    ans = bin(int(op0, 2) + int(op1, 2)).replace("0b", '')
    print("ans " , ans)
    op0len = op0.__len__() 
    op1len = op1.__len__()
    anslen = ans.__len__()
    isCarry = False
    isDecimal = False
    dec_value = ""
    if(isSignednumber):
        if(anslen > op1len):
            ans = ans[1:]
            isCarry = True
    final_ans= ""
    if(all_numbers[0][1] =="int" or all_numbers[1][1]=="int"):
        isDecimal = True
    print("isDecimal", isDecimal)
    steps="Steps:<br/>"
    if(all_numbers[0][1]=="int"):
        if(all_numbers[0][2] == "-"):
            steps = steps + "Convert to binary: -" + str(all_numbers[0][0]) + " ==> -" + str(binaries[0]) + "<br/>"
        else:
            steps = steps + "Convert to binary: " + str(all_numbers[0][0]) + " ==> " + str(binaries[0]) + "<br/>"
        if(all_numbers[0][2] =="-"):
            steps = steps + "Take two's compliment of negative number to get his binary representation: <br/> "
            steps = steps + str(binaries[0]) + " ==> " + result[0][0] + "<br/>"
    print("1 Steps " , steps)
    if(isDoubleNeg):
        steps = steps + "Double negation results in addition i.e. - -" + str(all_numbers[1][0]) + " ==> + " + str(all_numbers[1][0]) + "<br/>"
        if(all_numbers[1][2] == "-"):
            steps = steps + "so it is: " + str(all_numbers[0][2]) + str(all_numbers[0][0]) + " + " + str(all_numbers[1][0]) + "<br/>"
        else:
            steps = steps + "so it is: " + str(all_numbers[0][0]) + " + " + str(all_numbers[1][0]) + "<br/>"
    print("2 Steps " , steps)
    print(all_numbers[1])
    print(binaries)
    if(all_numbers[1][1]=="int"):
        if(all_numbers[0][2] == "-"):
            steps = steps + "Convert to binary: -" + str(all_numbers[1][0]) + " ==> -" + str(binaries[1]) + "<br/>"
        else:
            steps = steps + "Convert to binary: " + str(all_numbers[1][0]) + " ==> " + str(binaries[1]) + "<br/>"
        print("steps 2a " , steps)
        if(all_numbers[1][2] =="-"):
            steps = steps + "Take two's compliment of negative number to get his binary representation: <br/> "
            print("steps 2b " , steps)
            steps = steps + str(binaries[1]) + " ==> " + result[1][0] + "<br/>"
    print("3 Steps " , steps)
    steps = steps + "Adding numbers: <br/>"
    if(isCarry):
        steps = steps +  str(op0) + "<br/>"
        steps = steps +  str(op1) + "<br/>"
        steps = steps +  str(ans) + " Carry 1 discarded if it exceeds bits.<br/>"
    else:
        steps = steps +  str(op0) + "<br/>"
        steps = steps +  str(op1) + "<br/>"
        steps = steps +  str(ans) + "<br/>"
    if(isDecimal):
        dec_value = getDecimal(ans,isSignednumber)
    print("dec_value " , dec_value)
    
    
    return [ans, steps]

def binary_module(query):
    global required_bits
    global userbits

    isuserbit = False
    tokenize = nltk.word_tokenize(query)
    print(tokenize)
    for word in tokenize:
        bitindex = word.find("bit")
        bitindex1 = word.find("bits")
        if(bitindex > -1 and bitindex1 < 0):
            if(bitindex > 0):
                isuserbit = True
            user_bit= int(word[:bitindex])
            userbits= user_bit
            if(user_bit > required_bits):
                required_bits = user_bit
    if(isuserbit == False):
        required_bits=0
    kwd = [x for x in tokenize if x in keyword_list] # get common keywords
    print(kwd) 
          
    binar_numbers = []
    binar_signed =[]
    decimal_numbers = []
    decimal_signed =[]
    all_numbers=[]
    # isolate decimal and binary number arguments. 
    for i in tokenize:
        isSigned = False

        if i[0]== '-':
            isSigned = True
            i = i[1:]
        if re.match(r'[0-9]', i): 
            print("number: " , i)
            if check_binary_format(i) == "yes" and "base10" not in query and "base ten" not in query:
                print("binary: " , i)
                if(i.find("bit") < 0 ):
                    if ((len(i) < required_bits) and ('sum' not in kwd and '+'  not in kwd and "difference" not in kwd and "-" not in kwd)):
                        i.zfill(required_bits)
                    binar_numbers.append(i)
                    binar_signed.append(isSigned)
                    if(isSigned):
                        all_numbers.append([i,"bin","-"])
                    else:
                        all_numbers.append([i,"bin","+"])

            else:
                print("decimal: " , i)
                if(i.find("bit") < 0 ):
                    decimal_numbers.append(int(i))
                    decimal_signed.append(isSigned)
                    if(isSigned):
                        all_numbers.append([int(i),"int","-"])
                    else:
                        all_numbers.append([int(i),"int","+"])
    print(all_numbers)
            
    # print(binar_numbers, decimal_numbers)

    try:
        if (('one' in kwd or 'ones' in kwd or "one's" in kwd) or ('two' not in kwd and 'twos' not in kwd and "two's" not in kwd)) and ('compliment' in kwd or 'complement' in kwd):
            print("ones_compliment called")
            return one_compliment(binar_numbers, decimal_numbers)
    
        elif ('two' in kwd or 'twos' in kwd or "two's" in kwd) and ('compliment' in kwd or 'complement' in kwd):
            print("twos_compliment called")
            return twos_compliment(binar_numbers, decimal_numbers)

        elif 'bits' in kwd: 
            print("bit_representation called")
            return bit_representation(decimal_numbers)

        elif 'sum' in kwd or '+' in kwd:
            print("binary_addition called")
            return binary_add_sub("addition",all_numbers,binar_numbers,decimal_numbers)
        elif 'difference' in kwd or '-' in kwd:
            print("binary_subtraction called")
            return binary_add_sub("subtraction",all_numbers,binar_numbers,decimal_numbers)

        elif 'convert' in kwd or 'write' in kwd or 'represent':
            if "to decimal" in query or "binary to decimal" in query or 'decimal' in query: 
                print("binary_to_decimal called")
                return binary_to_decimal(binar_numbers, decimal_numbers)
            elif "to binary" in query or "decimal to binary" in query or 'binary' in query:
                print("decimal_to_binary called")
                return decimal_to_binary(decimal_numbers)
        else:
            return ["query format not correct, please repeat the question again.", ""]

    except:
        # raise Exception
        return ["Sorry, can you repeat your question", ""]


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
