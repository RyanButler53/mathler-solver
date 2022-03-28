OPERATORS = ['+', '-', '*', '/']
MULTDIV = ['*', '/']
ADDSUB = ['+', '-']

def evaluate(exp):
    """Evaluates the expression."""
    exp = [str(x) for x in exp] #make it a string, for testing purposes
    concatenated = [] #concatenated
    i = 0
    while i < 6: #concatenates the numbers
        if exp[i] in OPERATORS:
            concatenated.append(exp[i])
            i += 1
        else:
            numLength = 0
            num = ''
            #go until operator or end found
            while i + numLength < 6 and exp[i + numLength] not in OPERATORS:
                num += exp[i + numLength]
                numLength += 1
            concatenated.append(num)
            i += numLength
    multDiv = orderOfOperations(concatenated, MULTDIV)
    final = orderOfOperations(multDiv, ADDSUB)
    return int(final[0])
   

def orderOfOperations(exp, operations):
    while operations[0] in exp or  operations[1] in exp: #exactly 2 ops
        index = 0
        while index < len(exp):
            if exp[index] in operations:
                result = compute(int(exp[index-1]), int(exp[index+1]), exp[index])
                if result == False:
                    return [0]
                exp = exp[:index-1] + [result] + exp[index+2:]
            index += 1
    return exp

def compute(n1, n2, op):
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif n2 == 0:
        return False
    elif n1 % n2 != 0:
        return False
    else:
        return n1 // n2

#Now I need to search for solutions. 
#print possible solutions 
#Give information: Give correct indicies.  Give values that must be part of soln. 
#operators cannot be in first or last space. 
# operators cannot be right next to each other. 
#Can not start from scratch -- solution space is too large

def findSolutions(target, notInSoln, info):
    #Slow, non human brute force strategy
    """Finds the valid solutions for a given target with the information given
    target: And integer, the target value of the mathler puzzle
    notInSoln: List of ints and operators not in the solution """
    notInSoln = [str(x) for x in notInSoln]
    ints = list(filter(lambda nums: nums not in notInSoln, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']))
    ops = list(filter(lambda ops: ops not in notInSoln, OPERATORS))
    #find indicies solved: encoded as (index solved at, value at the index)
    #solved = [(i, value) for i, value, status in info if status == True]
    solved = {}
    solnList = []
    for i, value, status in info:
        if status == True:
            solved[i] = value
    firstChars = getValidChars(0, notInSoln, info, False, solved)
    for firstChar in firstChars:
        secondChars = getValidChars(1, notInSoln, info, False, solved)
        for secondChar in secondChars:
            if secondChar in OPERATORS:
                thirdChars = getValidChars(2, notInSoln, info, True, solved)
            else:
                thirdChars = getValidChars(2, notInSoln, info, False, solved)
            for thirdChar in thirdChars:
                if thirdChar in OPERATORS:
                    fourthChars = getValidChars(2, notInSoln, info, True, solved)
                else:
                    fourthChars = getValidChars(2, notInSoln, info, False, solved)
                for fourthChar in fourthChars:
                    if fourthChar in OPERATORS:
                        fifthChars = getValidChars(2, notInSoln, info, True, solved)
                    else:
                        fifthChars = getValidChars(2, notInSoln, info, False, solved)
                    for fifth in fifthChars:
                        finalChars =getValidChars(0, notInSoln, info, True, solved)
                        for final in finalChars: 
                            #print([firstChar, secondChar, thirdChar, fourthChar, fifth, final])
                            if evaluate([firstChar, secondChar, thirdChar, fourthChar, fifth, final]) == target:
                                #print([firstChar, secondChar, thirdChar, fourthChar, fifth, final])
                                solnList += [[firstChar, secondChar, thirdChar, fourthChar, fifth, final]]
    return solnList

def concatenateExp(exp):
    exp = [str(x) for x in exp] #make it a string, for testing purposes
    concatenated = [] #concatenated
    i = 0
    while i < 6: #concatenates the numbers
        if exp[i] in OPERATORS:
            concatenated.append(exp[i])
            i += 1
        else:
            numLength = 0
            num = ''
            #go until operator or end found
            while i + numLength < 6 and exp[i + numLength] not in OPERATORS:
                num += exp[i + numLength]
                numLength += 1
            concatenated.append(num)
            i += numLength
    return concatenated
def getValidChars(index, notInSoln, info, lastOpp, solvedDict = {}):
    if index in list(solvedDict.keys()):
        return list(solvedDict[index])
    else:
        allInts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        invalidChars = [value for i, value, status in info if i == index]
        filterfunc = lambda x: x not in notInSoln and x not in invalidChars
        ints = list(filter(filterfunc, allInts))
        ops = list(filter(filterfunc, OPERATORS))
        all = ints + ops
        if index  == 0 and '0' in all:
            all = all[1:] #slow but fine
        if lastOpp == True and '0' in all:
            all = all[1:]
        if index in [0, 5] or lastOpp == True:
            all = list(filter(lambda char: char not in OPERATORS, all))
        return all
    
    
    
