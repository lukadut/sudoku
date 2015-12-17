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


def find_missing(sudoku, y, x):
    missing = []
    if(sudoku[y][x]!="0"):
        print("DEBUG dla x=",x, " y=",y, sudoku[y][x])
        return missing

    debugValues = list(range(1,10))
    numbers = [0]*9;
    x_ = math.floor(x/3)
    y_ = math.floor(y/3)
    for i in range(0,3):
        kwadrat=""
        for j in range(0,3):
            print("DEBUG",(i + y_*3),(j + x_*3), sudoku[i + y_*3][j + x_*3])
            number = int( sudoku[i + y_*3][j + x_*3])
            kwadrat+=sudoku[i + y_*3][j + x_*3]
            if (number >0):
                numbers[number-1] +=1
        print("kwadrat",kwadrat)
    linia1= ""
    linia2 = ""
    for i in range (0,9):
        number = int(sudoku[i][x])
        numbers[number-1] +=1
        number = int(sudoku[y][i])
        numbers[number-1] +=1

        linia1+=sudoku[i][x]
        linia2+=sudoku[y][i]
    print("DEBUG dla x=",x, " y=",y, "LINIA 1", linia1, "LINIA2", linia2)

    for i in range(0,9):
        if(x == 1 and y==4):
            print("######DEBUG$$$$$", numbers)
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


    for index in indexes:
        #print("index",index[1])
        missing = find_missing(sudoku, index[0], index[1])
        #missing = find_missing(sudoku,1,8)

        print("index ", index," mozliwe wartosci " , missing)
        if(len(missing)==1):
            print("jedyna wartosc tutaj to", missing[0])
            string=""
            print(string + str(missing[0]))
            sudoku[index[0]][index[1]]=str(missing[0])
        else:
            string=""

        #print(" mozliwe wartosci " + find_missing(sudoku, index[0]+1, index[1]+1))
        #print(sudoku[index[0]][index[1]])

        #sudoku[index[0]][index[1]]=""
        #index = find_zeros(sudoku)
    return sudoku




if __name__ == '__main__':
    input = "sudoku.txt"
    sudoku = read_file(input)
    print_sudoku(sudoku)

    #find_missing(sudoku,0,7)

    #sudoku = resolver(sudoku)
    #print("###################")
    #sudoku = resolver(sudoku)

    print_sudoku(sudoku)




