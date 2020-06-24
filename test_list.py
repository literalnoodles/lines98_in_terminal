import json,os,time
from termcolor import colored
with open('name.json') as data_file:
    data = json.load(data_file)

def print_grid(arr):
    row = len(arr)
    col = len(arr[0])
    str = '+---'*col+'+\n'
    for i in range(row):
        for j in range(col):
            if (arr[i][j]==1):
                str += '| ' + colored('o','blue') + ' '
            elif (arr[i][j]==2):
                str += '| ' + colored('x','red') + ' '
            else:
                str += '|   '
        str += f'|{i}\n' + '+---'*col + '+\n'
    for i in range(col):
        str += f'  {i} '
    print(str)

#define the size of the matrix
MATRIX_ROW = len(data)
MATRIX_COL = len(data[0])

# define the movement
mx=[0,1,0,-1]
my=[-1,0,1,0]

#define the node data type
class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def find_path(s_node,e_node):
    # define the queue and add the start node to it
    x_queue = [s_node.x]
    y_queue = [s_node.y]

    # check if e_node is already exist
    # check if s_node is not exist
    if (data[e_node.x][e_node.y] or not data[s_node.x][s_node.y]):
        return []

    # defind the visited matrix
    visited = [[False for j in range(MATRIX_COL)] for i in range(MATRIX_ROW)]
    visited[s_node.x][s_node.y] = True

    # construct the prev matrix
    prev = [[None for j in range(MATRIX_COL)] for i in range(MATRIX_ROW)]

    #while the queue is not empty, continue explore all the adjacent
    while (x_queue):
        # get the current Node
        c_node = Node(x_queue.pop(0),y_queue.pop(0))
        if (c_node.x == e_node.x and c_node.y == e_node.y):
            break
        for i in range(4):
            # except out of range
            if c_node.x + mx[i] < 0: continue
            if c_node.x + mx[i] >= MATRIX_ROW : continue
            if c_node.y + my[i] < 0 : continue
            if c_node.y + my[i] >= MATRIX_COL : continue

            # except all block node
            x = c_node.x + mx[i]
            y = c_node.y + my[i]
            if data[x][y] == 1 : continue

            # except visited node
            if not visited[x][y]:
                # add to the queue
                x_queue.append(x)
                y_queue.append(y)

                #add to the visited
                visited[x][y] = True

                #construct the prev
                prev[x][y] = c_node
    
    #return the path
    trace_node = Node(e_node.x,e_node.y)
    reconstruct = []
    while (prev[trace_node.x][trace_node.y] != None):
        reconstruct.insert(0,trace_node)
        trace_node = prev[trace_node.x][trace_node.y]

    if not reconstruct:
        return []
    else:
        return reconstruct

def check_clear(node):
    drx = [
        [1,-1],
        [0,0],
        [1,-1],
        [-1,1]
    ]

    dry = [
        [0,0],
        [1,-1],
        [1,-1],
        [1,-1]
    ]

    for i in range(4):
        # check each direction
        total = 1
        total_in_line = [(node.x,node.y)]
        for j in range(2):
            c_posx = node.x
            c_posy = node.y
            while (True):
                c_posx += drx[i][j]
                c_posy += dry[i][j]
                # if the node is outside of the range -> break
                if (c_posx >= MATRIX_ROW or c_posx < 0 or c_posy >= MATRIX_COL or c_posy < 0 or not data[c_posx][c_posy]):
                    break
                # if the node is check
                if (data[c_posx][c_posy]):
                    total += 1
                    total_in_line.append((c_posx,c_posy))
        if total >= 3:
            # clear the position
            for pos in total_in_line:
                data[pos[0]][pos[1]] = 2

def clean_up():
    for i in range(MATRIX_ROW):
        for j in range(MATRIX_COL):
            if data[i][j] == 2:
                data[i][j] = 0

os.system('color')
os.system('cls')
# for node in find_path(Node(1,0),Node(3,4)):
#     print(f'->({node.x}-{node.y})',end='')

def update_screen():
    print_grid(data)
    time.sleep(0.2)
    os.system('cls')

while True:
    print_grid(data)
    str=input()
    os.system('cls')
    arr=str.split(',')
    path = find_path(Node(int(arr[0]),int(arr[1])),Node(int(arr[2]),int(arr[3])))
    if not path:
        continue
    path.insert(0,Node(int(arr[0]),int(arr[1])))
    for i in range(len(path)-1):
        #set data of prev node to 0
        data[path[i].x][path[i].y] = 0
        data[path[i+1].x][path[i+1].y] = 1
        update_screen()
    check_clear(Node(int(arr[2]),int(arr[3])))
    update_screen()
    clean_up()
    update_screen()