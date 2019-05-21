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

def signed_ones_complement(decimal_numbers, all_numbers):
    global required_bits
    i = all_numbers[0]
    result = []
    steps = "For Negative number: First convert the number to its binary and than take its two's compliment. Then takes one's compliment.<br/>"
    if len(all_numbers) == 1:
        steps = steps + 'To convert decimal number into binary, divide the number by 2 repeatedly until<br />'
        steps = steps + 'remainder becomes smaller than 2. Then read all the carry in backward(bottom to top) direction.<br />' 
        steps = steps + ' For this example, <br /> <b>'
        num = all_numbers[0][0]
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
        answer = str(bin(all_numbers[0][0]).replace("0b", ""))
        anslen = len(answer) + 1
        
        r_bit = anslen
        if(anslen < required_bits):
            r_bit = required_bits
            answer = answer.zfill(required_bits)
        else:
            answer = answer.zfill(anslen)
        steps = steps + "Now take twos compliment of " + answer + "<br/>"
        result.append(getBinTwosComplement(answer,r_bit))
        steps = steps + result[0][1]
        steps = steps + answer + " ==> " + result[0][0]   
        steps = steps + "<br/>Now take one's complement for final answer: "
        answer = result[0][0]
        a = answer
        temp = ""
        for i in range(0, len(a)):
            if a[i] == '0':
                temp = temp + '1'
            else: 
                temp = temp + '0'
        steps = steps + "<br/> invert every bit of the given bit string i.e change 0 to 1 and 1 to 0 : <br />" + a + " ==> " +  temp 
        steps = steps + "<br/> Convert decimal to binary"
        answer = temp
        ans = answer
        steps = steps + ""
        next_step = "= "
        if(ans[0]=='1'):
            answer = int(math.pow(2, len(ans)-1)) * -1 
            steps = steps +" "+ ans + "= - ( 2^" + str(len(ans)-1) + " * " + ans[0]+" ) " 
            next_step = next_step + "- " + str(int(math.pow(2, len(ans)-1)))
        else:
            steps = steps + "- ( 2^" + str(len(ans)-1) + " * " + ans[0]+" ) "
            next_step = next_step + "- 0"
        index= len(ans) - 1 
        index1= 1
        while (index > 1):
            steps = steps + "+ ( 2^" + str(index-1) + " * " + ans[index1]+" ) " 
            if(ans[index1]=="1"):
                answer = answer + int(math.pow(2, (index-1)) )
                next_step = next_step + " +  " + str(int(math.pow(2, (index-1) )))
            else:
                next_step = next_step + " + 0"
            index1 = index1 + 1
            index = index - 1
        steps = steps + "+ ( 2^0"  + " * " + ans[len(ans)-1]+" )<br/>" 
        if(ans[len(ans)-1] == "1"):
            answer = answer + 1
            next_step = next_step + " + 1<br/>"  
        else:
            next_step = next_step + " + 0<br/>"  
        next_step = next_step + " = " + str(answer) + "<br/>" 
        steps = steps + next_step
        final_ans = "Base 2 ( " + ans + " ), Base 10 ( " + str(answer) + ")" 
    else: 
        return ["Error! 1 argument required, given 0 or more than 1", ""]
    return [final_ans, steps]

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

def signed_decimal_to_binary(decimal_numbers, all_numbers):
    global required_bits
    i = all_numbers[0]
    result = []
    steps = "For Negative number: First convert the number to its binary and than take its two's compliment.<br/>"
    if len(decimal_numbers) == 1:
        steps = steps + 'To convert decimal number into binary, divide the number by 2 repeatedly until<br />'
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
        answer = str(bin(decimal_numbers[0]).replace("0b", ""))
        anslen = len(answer) + 1
        r_bit = anslen
        print("r_bit" , r_bit)
        if(anslen < required_bits):
            r_bit = required_bits
            answer = answer.zfill(required_bits)
        else:
            answer = answer.zfill(anslen)
        steps = steps + "Now take twos compliment of " + answer + "<br/>"
        result.append(getBinTwosComplement(answer,r_bit))
        steps = steps + result[0][1]
        steps = steps + answer + " ==> " + result[0][0]        
        print("STEPS " , steps)
        print("1 answer " , answer)
        answer = result[0][0]
        print("2 answer " , answer)


    else: 
        return ["Error! 1 argument required, given 0 or more than 1", ""]
    return [answer, steps]


def one_compliment(x, y = None):
    global required_bits
    if len(x) == 1:
        a = x[0]
        a = a.zfill(required_bits)
        temp = ""
        for i in range(0, len(a)):
            if a[i] == '0':
                temp = temp + '1'
            else: 
                temp = temp + '0'
        result = "invert every bit of the given bit string i.e change 0 to 1 and 1 to 0 : <br />" + a + " ==> " +  temp

        return [temp,result] 
    
    elif len(y) == 1:
        temp = bin(int(y[0])).replace("0b", "")
        temp = temp.zfill(required_bits)
        temp2 = ""

        for i in range(0, len(temp)):
            if temp[i] == '0':
                temp2 = temp2 + '1'
            else: 
                temp2 = temp2 + '0'
        

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

def bit_representation(decimal_numbers,all_numbers):
    if len(decimal_numbers) == 1:    
        steps = "Take log base 2 of the given binary string i.e log<sub>2</sub>(" + str(decimal_numbers[0]) + " + 1) = " + str(math.log(decimal_numbers[0]+1, 2)) 
        steps = steps + "<br />take ceiling of the previous result like this: &lceil;" + str(math.log(decimal_numbers[0] + 1, 2) ) + "&rceil; = " + str(math.ceil(math.log(decimal_numbers[0] + 1, 2 )))         
        answer = str(math.ceil(math.log(decimal_numbers[0] + 1, 2)))
        if(all_numbers[0][2] == "-"):
            steps = steps + "<br/>Since its a negative number: there is atleast 1 extra bit needed to represent it. So answer: " + str(math.ceil(math.log(decimal_numbers[0] + 1, 2)) + 1)
            answer = str(int(answer) + 1)
        steps = steps + "<br /> <b>Note: The answer has to be a integer, so we round up to the nearest biggest integer.</b>"
        return [answer, steps]
    
    else: 
        return ['Error! 1 arg required, given 0', ""]

def getBinTwosComplement(num, reqBit):
    steps = "apply one's compliment to binary string first and then add 1 to LSB (Least Significant Bit)<br />"
    num = num.zfill(reqBit)
    if(userbits > num.__len__()+1):
        num = num.zfill(userbits)
    else:
        num = num.zfill(num.__len__()+1)
    a = num
    temp = ""
    for i in range(0, len(a)):
        if a[i] == '0':
            temp = temp + '1'
        else: 
            temp = temp + '0'
    bitlen = temp.__len__()
    answer = str(bin(int(temp, base = 2) + 1).replace('0b', ''))
    if(len(answer) > reqBit):
        answer = answer[1:]
    answer = answer.zfill(bitlen)
    answer = answer.zfill(required_bits)
    return [answer , steps ,"bin"]

def getIntTwosComplement(num, reqBit):
    global userbits
    temp = bin(num).replace("0b", "")
    temp=temp.zfill(reqBit)
    a = temp
    temp = ""
    for i in range(0, len(a)):
        if a[i] == '0':
            temp = temp + '1'
        else: 
            temp = temp + '0'
    sum = int("0b" + temp, base = 2) + 1

    result = decimal_to_binary([sum])
    binary_res = result[0]
    if(len(binary_res)> reqBit):
        binary_res = binary_res[1:]
    if(userbits > binary_res.__len__()+1):
        binary_res = binary_res.zfill(userbits)
    steps = "First, convert decimal number into binary number.<br />"\
        "To convert decimal number into binary, "
    steps = steps + result[1] 
    steps = steps + "<br /> Then, apply one's compliment to binary string and then add 1 to LSB (Least Significant Bit) to get its negative representation i.e. " + binary_res
    steps = steps + binary_to_decimal([binary_res])[1]
    return [binary_res, steps,"int", str(sum)]


def getDecimal(num,isSigned):
    numLen = num.__len__()
    decimal_rep=""
    if(isSigned):
        if(num[0] == "0"):
            decimal_rep = str(int(num, base = 2))
        else:
            num1 = ""
            num1 = num1.zfill(numLen) 
            num1 = '1' + num1[1:]
            dec1 = int(num1, base = 2) * -1
            num = '0' + num[1:]
            dec = int(num, base = 2)
            decimal_rep = str(dec1 + dec)
    else:
        decimal_rep = str(int(num, base = 2))
    return decimal_rep


def binary_add_sub(op_type,all_numbers,binary_numbers,decimal_numbers = None):
    if(all_numbers.__len__() < 2):
        return ["Error: Not enough operands" ,""]
    isDoubleNeg = False
    global userbits
    global isSignednumber
    two_comp = 0
    isSignednumber = False
    if(all_numbers[1][2]=="-"):
        print("isSignednumber 1")
        isSignednumber = True
    result = []
    if(op_type == "subtraction"):
        if(all_numbers.__len__() > 1):
            if(all_numbers[1][2]=="-"):
                isDoubleNeg = True
                op_type = "addition"
                all_numbers[1][2] = "+"
            else:
                op_type = "addition"
                all_numbers[1][2] = "-"
    print(all_numbers)
    if(all_numbers[1][2]=="-" or all_numbers[0][2]=="-"):
        print("isSignednumber 2")
        isSignednumber = True
    binaries=[]
    for i in all_numbers:
        if(i[2] == "-"):
            if(i[1] == "int"):
                bin_rep = decimal_to_binary([i[0]])
                r_bit=bin_rep[0].__len__()+1
                if(userbits > r_bit):
                    r_bit = userbits
                i.append(r_bit)
                binaries.append(bin_rep[0])
            else:
                r_bit=i[0].__len__()+1
                if(userbits > r_bit):
                    r_bit = userbits
                i.append(r_bit)
                binaries.append(i[0])
        else:
            if(i[1] == "int"):
                bin_rep = decimal_to_binary([i[0]])
                r_bit=bin_rep[0].__len__()
                if(userbits > r_bit):
                    r_bit = userbits
                i.append(r_bit)
                binaries.append(bin_rep[0])
            else:
                r_bit=i[0].__len__()
                if(userbits > r_bit):
                    r_bit = userbits
                i.append(r_bit)
                binaries.append(i[0])
    if(all_numbers[0][3] < all_numbers[1][3]):
        all_numbers[0][3] = all_numbers[1][3]
    else:
        all_numbers[1][3] = all_numbers[0][3]
    for i in all_numbers:
        if(i[2] == "-"):
            two_comp = two_comp + 1
            if(i[1] == "int"):
                print("i[3] ", i[3])
                result.append(getIntTwosComplement(i[0],i[3]))
            else:
                result.append(getBinTwosComplement(i[0],i[3]))
        else:
            if(i[1] == "int"):
                bin_rep = decimal_to_binary([i[0]])
                bin_rep[0] = bin_rep[0].zfill(i[3])
                result.append([bin_rep[0], bin_rep[1],"int", str(i[1])])
            else:
                i[0] = i[0].zfill(i[3])
                result.append([i[0] , "" ,"bin"])
    
    op0 = result[0][0]
    op1 = result[1][0]
    op0len = op0.__len__() 
    op1len = op1.__len__()
    if(op0len > op1len):
        op1 = op1.zfill(op0len)
    else:
        op0 = op0.zfill(op1len)
    ans = bin(int(op0, 2) + int(op1, 2)).replace("0b", '')
    op0len = op0.__len__() 
    op1len = op1.__len__()
    anslen = ans.__len__()
    isCarry = False
    isDecimal = False
    dec_value = ""
    if(isSignednumber):
        if(anslen > op1len):
            isCarry = True
    final_ans= ""
    if(all_numbers[0][1] =="int" or all_numbers[1][1]=="int"):
        isDecimal = True
    steps=""
    if(all_numbers[0][1]=="int"):
        if(all_numbers[0][2] == "-"):
            steps = steps + "Operand 1 : Convert to binary: -" + str(all_numbers[0][0]) + " ==> -" + str(binaries[0]) + "<br/>"
        else:
            steps = steps + "Operand 1 : Convert to binary: " + str(all_numbers[0][0]) + " ==> " + str(binaries[0]) + "<br/>"
        if(all_numbers[0][2] =="-"):
            steps = steps + "Take two's compliment of negative number to get his binary representation: <br/> "
            steps = steps + str(binaries[0]) + " ==> " + result[0][0] + "<br/>"
    if(isDoubleNeg):
        steps = steps + "Double negation results in addition i.e. - -" + str(all_numbers[1][0]) + " ==> + " + str(all_numbers[1][0]) + "<br/>"
        if(all_numbers[1][2] == "-"):
            steps = steps + "so it is: " + str(all_numbers[0][2]) + str(all_numbers[0][0]) + " + " + str(all_numbers[1][0]) + "<br/>"
        else:
            steps = steps + "so it is: " + str(all_numbers[0][0]) + " + " + str(all_numbers[1][0]) + "<br/>"
    if(all_numbers[1][1]=="int"):
        if(all_numbers[1][2] == "-"):
            steps = steps + "Operand 2 : Convert to binary: -" + str(all_numbers[1][0]) + " ==> -" + str(binaries[1]) + "<br/>"
        else:
            steps = steps + "Operand 2 : Convert to binary: " + str(all_numbers[1][0]) + " ==> " + str(binaries[1]) + "<br/>"
        if(all_numbers[1][2] =="-"):
            steps = steps + "Take two's compliment of negative number to get his binary representation: <br/> "
            steps = steps + str(binaries[1]) + " ==> " + result[1][0] + "<br/>"
    steps = steps + "Adding numbers: <br/>"
    print("1 issigned " , isSignednumber )
    if(isSignednumber):
        steps = steps + "0" + str(op0) + "<br/>"
        steps = steps +  "0" + str(op1) + "<br/>"
        steps = steps +  str(ans) + "<br/>"
        temp_ans = ans[1:]
        
        if (two_comp == 1):
            steps = steps + "As there was only one negative operand, we are discarding the carry."
            ans = temp_ans
        answer = 0 
        prev_steps = steps
        steps = "<br/>Converting the number to its decimal value: <br/>"
        next_step = "= "
        if(ans[0]=='1'):
            answer = int(math.pow(2, len(ans)-1)) * -1 
            steps = steps +" "+ ans + "= - ( 2^" + str(len(ans)-1) + " * " + ans[0]+" ) " 
            next_step = next_step + "- " + str(int(math.pow(2, len(ans)-1)))
        else:
            steps = steps + "- ( 2^" + str(len(ans)-1) + " * " + ans[0]+" ) "
            next_step = next_step + "- 0"
        index= len(ans) - 1 
        index1= 1
        while (index > 1):
            steps = steps + "+ ( 2^" + str(index-1) + " * " + ans[index1]+" ) " 
            if(ans[index1]=="1"):
                answer = answer + int(math.pow(2, (index-1)) )
                next_step = next_step + " +  " + str(int(math.pow(2, (index-1) )))
            else:
                next_step = next_step + " + 0"
            index1 = index1 + 1
            index = index - 1
        steps = steps + "+ ( 2^0"  + " * " + ans[len(ans)-1]+" )<br/>" 
        if(ans[len(ans)-1] == "1"):
            answer = answer + 1
            next_step = next_step + " + 1<br/>"  
        else:
            next_step = next_step + " + 0<br/>"  
        next_step = next_step + " = " + str(answer) + "<br/>" 
        steps = steps + next_step

    else:
        op0len = len(op0)
        op1len = len(op1)
        anslen = len(ans)
        maxlen = op0len
        if(maxlen<op1len): 
            maxlen = op0len
        elif(maxlen<anslen):
            maxlen = anslen
        op0=op0.zfill(maxlen)
        op1=op1.zfill(maxlen)
        ans=ans.zfill(maxlen)
        steps = steps +  str(op0) + "<br/>"
        steps = steps +  str(op1) + "<br/>"
        steps = steps +  str(ans) + "<br/>"
        print("ans: " + ans)
        answer = 0 
        prev_steps = steps
        steps = "Converting the number to its decimal value: <br/> = "
        next_step = "= "
        index= len(ans)
        index1= 0
        while (index > 1):
            print("ans[index1] " , ans[index1])
            steps = steps + "( 2^" + str(index-1)  + " * " + ans[index1]+" ) + " 
            if(ans[index1]=="1"):
                answer = answer + int(math.pow(2, (index-1)) )
                next_step = next_step + " " + str(int(math.pow(2, (index-1) ))) + " + "
            else:
                next_step = next_step + " 0 + "
            index1 = index1 + 1
            index = index - 1
        print("ans[index1] " , ans[index1])
        steps = steps + "( 2^0"  + " * " + ans[len(ans)-1]+" ) <br/>" 
        if(ans[len(ans)-1] == "1"):
            answer = answer + 1
            next_step = next_step + " 1<br/>"  
        else:
            next_step = next_step + " 0<br/>"  
        next_step = next_step + " = " + str(answer) + "<br/>" 
        steps = steps + next_step
        
    
    if(isDecimal):
        #dec_value = getDecimal(ans,isSignednumber)
        prev_steps = prev_steps + steps 
        steps = prev_steps
        final_ans = "Base 2 ( " + ans + "), Base 10 ( " + str(answer) + " )"
    else:
        steps = prev_steps
        final_ans = ans
    
    
    return [final_ans, steps]

def binary_module(query):
    global required_bits
    global userbits
    global default_bits
    global isSignednumber
    required_bits= 4
    default_bits = 0
    isSignednumber = False
    userbits = 0
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
            if check_binary_format(i) == "yes" and "base10" not in query and "base ten" not in query:
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
                if(i.find("bit") < 0 ):
                    decimal_numbers.append(int(i))
                    decimal_signed.append(isSigned)
                    if(isSigned):
                        all_numbers.append([int(i),"int","-"])
                    else:
                        all_numbers.append([int(i),"int","+"])
            
    # print(binar_numbers, decimal_numbers)

    try:
        if (('one' in kwd or 'ones' in kwd or "one's" in kwd) or ('two' not in kwd and 'twos' not in kwd and "two's" not in kwd)) and ('compliment' in kwd or 'complement' in kwd):
            if(all_numbers[0][2] == "-"):
                return signed_ones_complement(decimal_numbers, all_numbers)
            else:
                return one_compliment(binar_numbers, decimal_numbers)
    
        elif ('two' in kwd or 'twos' in kwd or "two's" in kwd) and ('compliment' in kwd or 'complement' in kwd):
            return twos_compliment(binar_numbers, decimal_numbers)

        elif 'bits' in kwd: 
            return bit_representation(decimal_numbers,all_numbers)

        elif 'sum' in kwd or '+' in kwd:
            return binary_add_sub("addition",all_numbers,binar_numbers,decimal_numbers)
        elif 'difference' in kwd or '-' in kwd:
            return binary_add_sub("subtraction",all_numbers,binar_numbers,decimal_numbers)

        elif 'convert' in kwd or 'write' in kwd or 'represent':
            if "to decimal" in query or "binary to decimal" in query or 'decimal' in query: 
                return binary_to_decimal(binar_numbers, decimal_numbers)
            elif "to binary" in query or "decimal to binary" in query or 'binary' in query:
                if(all_numbers[0][2] == "-"):
                    return signed_decimal_to_binary(decimal_numbers,all_numbers)
                else:
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
