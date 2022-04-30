import copy
import operator
import random

class evalue:
    def __init__(self):
        self.steps = 0
        self.solved = 0
sc = evalue()

class point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = []
        self.value = 0




def rowNum(p, sudoku):

    row = set(sudoku[p.y * 9:(p.y + 1) * 9])
    if int(0) in row:
        row.remove(0)
    return row  # set type


def colNum(p, sudoku):

    col = []
    length = len(sudoku)
    for i in range(p.x, length, 9):
        col.append(sudoku[i])
    col = set(col)
    if int(0) in col:
        col.remove(0)
    return col  # set type


def blockNum(p, sudoku):
    block_x = p.x // 3
    block_y = p.y // 3
    block = []
    start = block_y * 3 * 9 + block_x * 3
    for i in range(start, start + 3):
        block.append(sudoku[i])
    for i in range(start + 9, start + 9 + 3):
        block.append(sudoku[i])
    for i in range(start + 9 + 9, start + 9 + 9 + 3):
        block.append(sudoku[i])
    block = set(block)
    if int(0) in block:
        block.remove(0)
    return block  # set type


def initPoint(sudoku):
    pointList = []
    length = len(sudoku)
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    p.available.append(j)
            pointList.append(p)
    return pointList
    

def getPossible(p,sudoku):
    s1 = rowNum(p, sudoku)
    s2 = colNum(p, sudoku)
    s3 = blockNum(p, sudoku)
    s4 = (s1|s2|s3)
    lis = list(s4)
    num = [1,2,3,4,5,6,7,8,9]
    list1 = []
    for i in num:
        if not i in lis:
            list1.append(i)
    return list1

def ForwardCheck1(sudoku):
    sodu = sudoku
    estva(sodu,0)
    return sodu

def ForwardCheck(pointList, sudoku):
    
    updatedList = []
    sudoku = ForwardCheck1(sudoku)
    updatedList = initPoint(sudoku)
    return updatedList

def estva(sudo,pos):
    if pos == 81:
        return True
    a = pos//9
    b = pos%9
    if(sudo[a*9+b]) !=0:
        return estva(sudo,pos+1)
    p = point(b,a)
    ls = getPossible(p,sudo)
    for i in ls:
        sudo[a*9+b] = i
        if(estva(sudo,pos+1)):
            return True
    sudo[a*9+b] = 0
    return False
    

def BacktrackCSP_frameWork(pointList, sudoku, select=None):
    if len(pointList) <= 0:
        return True
    #Select the next unassigned variable
    if select == "default": #default function, just use it to support your understanding.
        pselected = select_unassigned_var(pointList, sudoku)
    elif select == "MRV":
        pselected = select_unassigned_var_MRV(pointList, sudoku)
    elif select == "New":
        pselected = select_unassigned_var_New(pointList, sudoku)
    else:
        print("select method undefined!")
        return
    flag = False
    


    num = pselected.available
    x1 = pselected.x
    y1 = pselected.y
    random.shuffle(num)
    for x in num:
        pselected.value = x
        sc.steps +=1
        sudokuCopy = copy.copy(sudoku)
        if check(pselected,sudoku) == True:                               
            sudoku[x1+y1*9] = pselected.value
            pointList = ForwardCheck(pointList, sudoku)
            result = BacktrackCSP_frameWork(pointList, sudoku, select)
            if result != True:            
                return result

        
    return flag


def testSudoku(sudoku):

    for i in range(9):
        nums=set()
        for j in range(9):
            if sudoku[i*9+j]==0:
                print("(%d,%d) is 0"%(i,j))
                print(sudoku)
                return False
            nums.add(sudoku[i*9+j])
        if len(nums)<9:
            print("row: %d"%i)
            return False
    for i in range(9):
        nums=set()
        for j in range(9):
            if sudoku[i + j*9] == 0:
                print("(%d,%d) is 0" % (j, i))
                print(sudoku)
                return False
            nums.add(sudoku[i+j*9])
        if len(nums)<9:
            print("col:%d"%i)
            return False
    for i in range(0,9,3):
        for j in range(0,9,3):
            nums=set()
            nums.update({sudoku[i*9+j], sudoku[i*9+j+1], sudoku[i*9+j+2],
                         sudoku[(i+1)*9+j],sudoku[(i+1)*9+j+1],sudoku[(i+1)*9+j+2],
                         sudoku[(i+2)*9+j],sudoku[(i+2)*9+j+1],sudoku[(i+2)*9+j+2]
                         })
            nums.difference_update({0})
            if len(nums)<9:
                print("(%d,%d)block:"%(i,j))
                return False
    return True

def select_unassigned_var(pointList, sudoku):

    return pointList.pop()


def select_unassigned_var_MRV(pointList, sudoku):
    cmpfun = operator.attrgetter('available')
    pointList.sort(key=cmpfun)
    return pointList.pop()



def select_unassigned_var_New(pointList, sudoku):
    if len(pointList)>0:
        i = random.randrange(0, len(pointList))
        a = pointList[i]
        pointList[-1] = pointList[i]
        pointList[i] = pointList[-1]
    return pointList.pop()



def checkRuleOut(sudoku, pointList):
    length = len(sudoku)
    count = 0
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    count += 1
    oldCount = 0
    for k in pointList:
        oldCount += len(k.available)

    return oldCount - count



def check(p, sudoku):
    """Check if position p's trial value violate rules, return True if not violated"""
    if p.value == 0:
        print('in value to point p!!')
        return False
    if p.value not in rowNum(p, sudoku) and p.value not in colNum(p, sudoku) and p.value not in blockNum(p, sudoku):
        return True
    else:
        return False


def showSudoku(sudoku):
    """Print the sudoku"""
    for j in range(9):
        for i in range(9):
            print('%d ' % (sudoku[j * 9 + i]), end='')
        print('')
    print("\n")

