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
    opt(str1,str2)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken


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
    


def init_array():
    global arr, str1, str2
    arr = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]
    for i in range(1, len(str1) + 1):
        arr[i][0] = i * DELTA
    for j in range(1, len(str2) + 1):
        arr[0][j] = j * DELTA



def opt(str1, str2):
    global arr
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            arr[i][j] = min((arr[i-1][j-1] + get_cost(str1[i-1], str2[j-1])), (arr[i-1][j] + DELTA), (arr[i][j-1] + DELTA))


def printStrings():
    global arr, str1, str2
    aligned1 = ""
    aligned2 = ""
    i,j = len(str1), len(str2)
    
    while i > 0 and j > 0:
        s = arr[i][j]
        if s == arr[i-1][j-1] + get_cost(str1[i-1], str2[j-1]):
            aligned1 = str1[i-1] + aligned1
            aligned2 = str2[j-1] + aligned2
            i = i - 1
            j = j - 1
        elif i > 0 and s == arr[i-1][j] + DELTA:
            aligned1 = str1[i-1] + aligned1
            aligned2 = '_' + aligned2
            i = i - 1
        else:
            aligned1 = "_" + aligned1
            aligned2 = str2[j-1] + aligned2
            j = j - 1
            
    while i > 0:
        aligned1 = str1[i-1] + aligned1
        aligned2 = "_" + aligned2
        i = i - 1
    while j > 0:
        aligned1 = "_" + aligned1
        aligned2 = str2[j-1] + aligned2
        j = j - 1
        
    return aligned1, aligned2


input_file = sys.argv[1]
output_file = sys.argv[2]
DELTA = 30
arr = None

str1 = None
str2 = None

parse_file(input_file)
init_array()
time = time_wrapper(str1,str2)
w1,w2 = printStrings()

f = open(output_file, "w")
f.write(str(arr[-1][-1]) + "\n")
f.write(w1 + "\n")
f.write(w2 + "\n")
f.write(str(time) + "\n")
f.write(str(process_memory()))
f.close()

