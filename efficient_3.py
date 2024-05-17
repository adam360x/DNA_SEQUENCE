import sys
from resource import *
import time
import psutil

def process_memory():
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed


def time_wrapper(str1,str2): 
    start_time = time.time() 
    o1, o2 = dc(str1,str2)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken, o1, o2


def get_cost(i, j):
    cost = {
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
    }
    return cost[i][j]
        

def parse_file(filename):

    with open(filename, 'r') as file:
        str = None
        num = []
        
        for line in file:
            l = line.strip()
            if l.isdigit():
                num.append(int(l))
            else:
                if str is not None:
                    gen_input(str, num)
                str = l
                num = []
    
    if str is not None:
        gen_input(str, num)
   

def gen_input(baseString, insertions):

    global str1,str2

    for x in insertions:
        baseString = baseString[:(x+1)] + baseString + baseString[(x+1):]

    if str1 is None:
        str1 = baseString
    elif str2 is None:
        str2 = baseString

def nw(str1,str2):

    len1 = len(str1)
    len2 = len(str2)
    
    score = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(1, len1 + 1):
        score[i][0] = i * DELTA
    for i in range(1, len2 + 1):
        score[0][i] = i * DELTA
        
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            score[i][j] = min(score[i-1][j-1] + get_cost(str1[i-1], str2[j-1]), score[i-1][j] + DELTA, score[i][j-1] + DELTA)
    
    
    lr = score[-1]
    
    a1 = ""
    a2 = ""
    
    i = len1
    j = len2
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and score[i][j] == score[i-1][j-1] + get_cost(str1[i-1], str2[j-1]):
            a1 = str1[i-1] + a1
            a2 = str2[j-1] + a2
            i = i - 1
            j = j -1
        elif i > 0 and score[i][j] == score[i-1][j] + DELTA:
            a1 = str1[i-1] + a1
            a2 = "_" + a2
            i = i -1
        else:
            a1 = "_" + a1
            a2 = str2[j-1] + a2
            j = j -1
            
    return a1,a2, lr


def nws(str1,str2):
    _, _, ret = nw(str1,str2)
    return ret

def dc(str1,str2):
    
    if len(str1) == 0:
        return '_' * len(str2), str2
    elif len(str2) == 0:
        return str1, '_' * len(str1)
    elif len(str1) == 1 or len(str2) == 1:
        a1, a2, _ = nw(str1,str2)
        return a1,a2
    
    mid = len(str1) // 2
    
    ls = nws(str1[:mid], str2)
    lr = nws(str1[mid:][::-1], str2[::-1])
    lr = lr[::-1]
    mid2 = min(range(len(str2) + 1), key=lambda x: ls[x] + lr[x])
    
    ret11, ret12 = dc(str1[:mid], str2[:mid2])
    ret21, ret22 = dc(str1[mid:], str2[mid2:])
        
    return ret11 + ret21, ret12+ret22
        

def cost(str1, str2):
    
    t = 0

    for c1, c2 in zip(str1, str2):
        if c1 == '_' or c2 == '_':
            t = t + DELTA
        else:
            t = t + get_cost(c1, c2)

    return t


input_file = sys.argv[1]
output_file = sys.argv[2]
DELTA = 30
arr = None

str1 = None
str2 = None

parse_file(input_file)
time,w1,w2 = time_wrapper(str1,str2)


f = open(output_file, "w")
f.write(str(cost(w1,w2)) + "\n")
f.write(w1 + "\n")
f.write(w2 + "\n")
f.write(str(time) + "\n")
f.write(str(process_memory()))
f.close()

