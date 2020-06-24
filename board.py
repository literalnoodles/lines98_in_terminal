import json,random,os,time
from termcolor import colored
from Node import Node
def convert_index_to_pos(index,row,col):
    posx = index // col
    posy = index % col
    return (posx,posy)

class Board:
    def __init__(self,matrix_col,matrix_row):
        self.matrix_col = matrix_col
        self.matrix_row = matrix_row
        self.grid = [[None for j in range(matrix_col)] for i in range(matrix_row)]
        self.available = matrix_col * matrix_row
        self.gen_node(3,'o')
        self.gen_node(3,'-')

    def gen_node(self,number,ntype):
        for i in range(number):
            pos = random.randint(0,self.available-1)
            self.available -= 1
            c_pos = 0
            count = 0
            while (True):
                posx,posy = convert_index_to_pos(c_pos,self.matrix_row,self.matrix_col)
                if (not self.grid[posx][posy]):
                    count += 1
                if (count > pos):
                    break
                else:
                    c_pos += 1
            posx,posy = convert_index_to_pos(c_pos,self.matrix_row,self.matrix_col)
            color = random.randint(0,5)
            self.grid[posx][posy] = Node(ntype,color)

    def input_move(self):
        move = input('-> ')
        # sx, sy, ex, ey = [int(i) for i in move.split(",")]
        sx, sy, ex, ey = [int(_) for _ in move]
        path = self.find_path(int(sx),int(sy),int(ex),int(ey))
        if not path:
            return
        color = self.grid[sx][sy].color
        temp = None
        for i in range(1,len(path)):
            if (temp):
                self.grid[temp[0]][temp[1]] = Node("-",temp[2])
                temp = None
            if (self.grid[path[i][0]][path[i][1]] and self.grid[path[i][0]][path[i][1]].ntype == "-"):
                temp = (path[i][0], path[i][1], self.grid[path[i][0]][path[i][1]].color)
            # unset previous node
            if (self.grid[path[i-1][0]][path[i-1][1]] and self.grid[path[i-1][0]][path[i-1][1]].ntype == "o"):
                self.grid[path[i-1][0]][path[i-1][1]] = None
            self.grid[path[i][0]][path[i][1]] = Node("o",color)
            self.update_screen()
            time.sleep(0.5)
        clear = self.check_clear(ex,ey)
        if not clear:
            self.gen_node(3,"-")
        self.update_screen()

    def check_clear(self,x,y):
        clear = False
        color = self.grid[x][y].color
        for i in range(4):
            total = 1
            total_in_line = [(x,y)]
            for j in range(2):
                cx = x
                cy = y
                while (True):
                    cx += self.direction[i][j][0]
                    cy += self.direction[i][j][1]
                    # if out of bound break || null || different color
                    if (cx < 0
                        or cx >= self.matrix_row
                        or cy < 0
                        or cy >= self.matrix_col
                        or not self.grid[cx][cy]
                        or self.grid[cx][cy].ntype != "o"
                        or self.grid[cx][cy].color != color
                    ):
                        break
                    total += 1
                    total_in_line.append((cx,cy))
            if total > 3:
                clear = True
                for pos in total_in_line:
                    self.grid[pos[0]][pos[1]] = Node("x",0)
        self.update_screen()
        time.sleep(0.5)
        # for i in range(self.matrix_row):
        #     for j in range(self.matrix_col):
        #         if (self.grid[i][j] and self.grid[i][j].ntype == "x"):
        #             self.grid[i][j] = None
        #         if (self.grid[i][j] and self.grid[i][j].ntype == "-" and not clear):
        #             self.grid[i][j] = Node("o",self.grid[i][j].color)

        clear = self.clear(clear)
        self.update_screen()
        return clear
        # time.sleep(0.5)

    def clear(self,clear):
        if clear:
            for i in range(self.matrix_row):
                for j in range(self.matrix_col):
                    if (self.grid[i][j] and self.grid[i][j].ntype == "x"):
                        self.grid[i][j] = None
        else:
            newNodes = []
            for i in range(self.matrix_row):
                for j in range(self.matrix_col):
                    if (self.grid[i][j] and self.grid[i][j].ntype == "-"):
                        self.grid[i][j] = Node("o",self.grid[i][j].color)
                        newNodes.append((i,j))
            self.update_screen()
            time.sleep(0.5)
            for node in newNodes:
                clr = self.check_clear(node[0],node[1])
                if clr:
                    self.clear(True)
                    clear = True
        return clear
        # self.update_screen()
        # for i in range(self.matrix_row):
        #     for j in range(self.matrix_col):
        #         if (self.grid[i][j] and self.grid[i][j].ntype == "x"):
        #             self.grid[i][j] = None
        #         if (self.grid[i][j] and self.grid[i][j].ntype == "-" and not clear):
        #             self.grid[i][j] = Node("o",self.grid[i][j].color)
        # self.update_screen()
        # return clear

    def find_path(self,sx,sy,ex,ey):
        # if index out of bound -> return
        # if end node is "o" node -> return
        # if start node is None -> return
        if (
            sx < 0 
            or sx >= self.matrix_row
            or ex < 0
            or ex > self.matrix_row
            or sy < 0
            or sy >= self.matrix_col
            or ey < 0
            or ey >= self.matrix_col
            or (self.grid[ex][ey] and self.grid[ex][ey].ntype == "o")
            or not (self.grid[sx][sy] and self.grid[sx][sy].ntype == "o")
        ):
            return None
        x_queue = [sx]
        y_queue = [sy]

        visited = [[False for i in range(self.matrix_col)] for j in range(self.matrix_row)]
        visited[sx][sy] = True

        prev = [[None for i in range(self.matrix_col)] for i in range(self.matrix_row)]

        while(x_queue):
            cx = x_queue.pop(0)
            cy = y_queue.pop(0)
            # if current node is end node -> break the loop
            if (cx == ex and cy == ey):
                break
            for i in range(4):
                adj_x = cx + self.move[i][0]
                adj_y = cy + self.move[i][1]
                # if visited -> continue
                # if out of bound or "o" -> continue
                if (
                    adj_x < 0 or adj_x >= self.matrix_row
                    or adj_y < 0 or adj_y >= self.matrix_col
                    or visited[adj_x][adj_y]
                    or (self.grid[adj_x][adj_y] and self.grid[adj_x][adj_y].ntype == "o")
                ):
                    continue
                # add to the visited
                # add to the queue
                visited[adj_x][adj_y] = True
                x_queue.append(adj_x)
                y_queue.append(adj_y)
                prev[adj_x][adj_y] = (cx,cy)
        # return the path
        trace_path = []
        trace_x = ex
        trace_y = ey
        while (prev[trace_x][trace_y]):
            trace_path.insert(0,(trace_x,trace_y))
            trace_x,trace_y = prev[trace_x][trace_y]
        # while (trace_x != sx or trace_y != sy):
        #     trace_path.insert(0,(trace_x,trace_y))
        #     trace_x,trace_y = prev[trace_x][trace_y]
        if (trace_path):
            trace_path = [(sx,sy),*trace_path]
        # print(trace_path)
        # time.sleep(100000)
        return trace_path

    def print_grid(self):
        str = '+---'*self.matrix_col+'+\n'
        for i in range(self.matrix_row):
            for j in range(self.matrix_col):
                if not self.grid[i][j]:
                    str += '|   '
                else:
                    str += '| ' + colored(self.grid[i][j].ntype,Board.map_color(int(self.grid[i][j].color))) + ' '
            str += f'|{i}\n' + '+---'*self.matrix_col + '+\n'
        for i in range(self.matrix_col):
            str += f'  {i} '
        print(str)

    def update_screen(self):
        os.system('cls')
        self.print_grid()

    @staticmethod
    def map_color(index):
        cmap = {
            0 : "red",
            1 : "green",
            2 : "yellow",
            3 : "blue",
            4 : "magenta",
            5 : "cyan"
        }
        return cmap[index]

    @property
    def move(self):
        return [
            (1,0),
            (-1,0),
            (0,1),
            (0,-1)
        ]
    
    @property
    def direction(self):
        return [
            [(1,0),(-1,0)],
            [(0,1),(0,-1)],
            [(1,1),(-1,-1)],
            [(1,-1),(-1,1)]
        ]


