import copy
import math

def read_file(filename):
    with open(filename,'r') as f:
        data=[list(line.rstrip().ljust(9,'0')) for line in f]

    if(len(data)!=9):
        return -1

    for i in range(0,9):
        if (len(data[i]) >9):
            return -1
        for j in range(0,9):
            if not(str(data[i][j]).isnumeric() or str(data[i][j]).isspace() ):
                return -1
            #if (data[i][j]==' '):
             #   data[i][j]='0'

    return data

def print_sudoku(data):
    for j in range(0,9):
        line=""
        delim=""

        for i in range(0,9):
            line += data[j][i]
            if(i%3==2):
                line+="|"
            if((j%8)%3== 2):
                if(i%4 ==3):
                    delim+="+"
                else:
                    delim+="-"
        print(line[:-1])
        if(delim.__len__() > 0):
            delim+="--"
            print(delim)

def get_square(sudoku, y, x):
    values = []
    x_ = math.floor(x/3)
    y_ = math.floor(y/3)
    for i in range(0,3):
        for j in range(0,3):
            values+=(sudoku[i + y_*3][j + x_*3])
    return values

def get_line(sudoku,y,x):
    vertical=[]
    horizontal=[]
    for i in range (0,9):
        vertical+=sudoku[i][y]
        horizontal+=sudoku[x][i]
    return vertical,horizontal

def find_missing(sudoku, y, x):
    missing = []
    if(sudoku[y][x]!="0"):
        #print("ERROR dla x=",x, " y=",y, sudoku[y][x])
        return missing

    numbers = [0]*9;
    square = get_square(sudoku,y,x)
    #print("square",square)
    kwadrat=""
    for i in range(0,9):
        number = int( square[i])
        kwadrat+=square[i]
        if (number >0):
            numbers[number-1] +=1
            #print("DEBUG zwiekszam",number-1)
    #print("kwadrat",kwadrat)
    liniaV= ""
    liniaH = ""
    vertical, horizontal = get_line(sudoku,x,y)
    for i in range (0,9):
        number = int(vertical[i])
        if (number >0):
            numbers[number-1] +=1
            #print("DEBUG zwiekszam pion",number-1)
        number = int(horizontal[i])
        if (number >0):
            numbers[number-1] +=1
            #print("DEBUG zwiekszam poziom",number-1)

        liniaV+=vertical[i]
        liniaH+=horizontal[i]
    #print("DEBUG dla x=",x, " y=",y, "liniaV ", liniaV, "liniaH", liniaH)

    #print("numbers",numbers)

    for i in range(0,9):
        # if(x == 1 and y==4):
        #     print("######DEBUG$$$$$", numbers)
        if (numbers[i]==0):
            missing.append(i+1)
    #print(missing)
    return missing

def find_zeros(sudoku):
    index=[]
    for i in range(0,9):
        for j in range(0,9):
            if(sudoku[i][j]=="0"):
                index.append((i,j))
    return index

def find_zero(sudoku):
    for i in range(0,9):
        for j in range(0,9):
            return (i,j)

    return (-1,-1)

def resolver(sudoku):
    indexes = find_zeros(sudoku)
    #print("liczba zer", len(indexes))

    possible_values = ['']*9
    for x in range(0,9):
        #print(x)
        possible_values[x]= ['']*9

    for index in indexes:
            missing = find_missing(sudoku, index[0], index[1])
            possible_values[index[0]][index[1]] = missing

    while(len(find_zeros(sudoku))>0):
        flag = 0
        indexes = find_zeros(sudoku)

        missing_min_length = 9
        missing_min_index = [0, 0]

        for index in indexes:
            missing = find_missing(sudoku, index[0], index[1])

            if len(missing) < missing_min_length:
                missing_min_length = len(missing)
                missing_min_index = index

            #print("index ", index," mozliwe ", str(len(missing)), " wartosci " , missing)

            if(len(missing)==1):
                #print("jedyna wartosc tutaj to", missing[0])
                flag=1
                sudoku[index[0]][index[1]]=str(missing[0])

        if(flag == 0):
            #print("nie umiem",index)

            missing = find_missing(sudoku, missing_min_index[0], missing_min_index[1])
            #print("index ", missing_min_index," mozliwe ", str(len(missing)), " wartosci " , missing)

            for m in range(0, len(missing)):
                sudoku_copy = copy.deepcopy(sudoku)
                sudoku_copy[missing_min_index[0]][missing_min_index[1]]=str(missing[m])
                sudoku_result = resolver(sudoku_copy)

                if(len(find_zeros(sudoku_result))==0):
                    return sudoku_result

            return sudoku

    return sudoku

if __name__ == '__main__':
    input = "sudoku.txt"
    sudoku = read_file(input)
    print_sudoku(sudoku)

    print("\n#####################")
    print("Trwa rozwiązywanie...")
    print("#####################\n")

    sudoku = resolver(sudoku)
    print_sudoku(sudoku)
