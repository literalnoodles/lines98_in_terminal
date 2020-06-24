class Graph:
    def __init__(self,vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
    def add_edge(self,src,dest):
        self.graph[src].append(dest)
        
    def print_graph(self):
        for i in range(self.V):
            print(i,end="")
            for node in self.graph[i]:
                print(f'->{node}',end='')
            print('\n')
    
    def bfs(self,s_node):
        visited = [False for _ in range(self.V)]
        q = []
        prev = [None for _ in range(self.V)]
        q.append(s_node)
        visited[s_node] = True
        while (q):
            i = q.pop(0)
            # print(f'->{i}',end='')
            node = self.graph[i]
            for adj in node:
                if (not visited[adj]):
                    q.append(adj)
                    visited[adj] = True
                    prev[adj] = i 
        return prev
    def find_path(self,s_node,e_node):
        prev = self.bfs(s_node)
        index = e_node
        return_list = [e_node]
        while (prev[index] != None):
            # print(f'->{prev[index]}',end='')
            return_list.insert(0,prev[index])
            index = prev[index]
        return return_list if return_list[0] == s_node else []

g = Graph(4)
g.add_edge(0, 1) 
g.add_edge(0, 2) 
g.add_edge(1, 2) 
g.add_edge(2, 0) 
g.add_edge(2, 3) 
g.add_edge(3, 3)
# g.print_graph()
# print(g.bfs(2))
# g.find_path(1,3)
print(g.find_path(1,3))